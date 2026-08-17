import asyncio
import json
import time
from typing import List, Dict

from app.core.agent.graph import get_agent
from langchain_core.messages import HumanMessage

DATASET = [
    # --- 1. Greetings & Small Talk (5) ---
    {"type": "greeting", "query": "Hi there!"},
    {"type": "greeting", "query": "Hello, how can you help me today?"},
    {"type": "greeting", "query": "Good morning assistant."},
    {"type": "greeting", "query": "Hey! Who are you?"},
    {"type": "greeting", "query": "What's up?"},

    # --- 2. General FAQs & Real Estate Info (5) ---
    {"type": "faq", "query": "What is the difference between a carpet area and a super built-up area?"},
    {"type": "faq", "query": "Explain what a cap rate is in simple terms."},
    {"type": "faq", "query": "What are the hidden costs of buying a home in India?"},
    {"type": "faq", "query": "Should I rent or buy a house?"},
    {"type": "faq", "query": "What is a good CIBIL score for a home loan?"},

    # --- 3. Indian Property Search (Local DB + MagicBricks) (10) ---
    {"type": "search_in", "query": "Find me 2 BHK apartments in Bangalore under 80 Lakhs."},
    {"type": "search_in", "query": "Are there any villas for sale in Mumbai above 2 Cr?"},
    {"type": "search_in", "query": "Show me properties in Pune."},
    {"type": "search_in", "query": "I am looking for a 3 BHK in Delhi NCR budget 1.5 Cr."},
    {"type": "search_in", "query": "Find budget homes in Chennai under 40 lakhs."},
    {"type": "search_in", "query": "Look for luxury penthouses in Hyderabad above 5 Cr."},
    {"type": "search_in", "query": "Do you have any 1 BHK flats in Noida?"},
    {"type": "search_in", "query": "Find residential houses in Kolkata under 1 Cr."},
    {"type": "search_in", "query": "Search for properties in Gurgaon."},
    {"type": "search_in", "query": "Find 4 BHK apartments in Whitefield, Bangalore."},

    # --- 4. US Property Search (Zillow / Fallback) (5) ---
    {"type": "search_us", "query": "Find homes in Austin, TX under $500k."},
    {"type": "search_us", "query": "Are there any properties in New York for $1 million?"},
    {"type": "search_us", "query": "Show me 3 bed 2 bath houses in Seattle."},
    {"type": "search_us", "query": "Search live Zillow properties in Miami, FL."},
    {"type": "search_us", "query": "Look for condos in San Francisco under $800,000."},

    # --- 5. Mortgage Calculator (8) ---
    {"type": "mortgage", "query": "Calculate EMI for a ₹1.5 Cr home with ₹30L down payment at 8.5% interest over 20 years."},
    {"type": "mortgage", "query": "What will be my monthly payment for a $400k house, 20% down, 6.5% interest, 30-year term?"},
    {"type": "mortgage", "query": "If I buy a 80 Lakh flat with 10% down payment and 9% interest for 15 years, what's the EMI?"},
    {"type": "mortgage", "query": "Calculate mortgage for a ₹2.5 Cr villa, assuming 20% down and 8.5% interest over 25 years."},
    {"type": "mortgage", "query": "I want to buy a $600k condo. Assume $100k down, 7% interest for 30 years. What is the total cost?"},
    {"type": "mortgage", "query": "What's the EMI on a 50 Lakh loan at 8.25% for 20 years?"},
    {"type": "mortgage", "query": "Calculate the lifetime interest paid on a $300k loan at 6% over 15 years."},
    {"type": "mortgage", "query": "If I take a ₹1 Cr loan for 30 years at 8.75%, what will be my monthly payment?"},

    # --- 6. ROI Analysis (7) ---
    {"type": "roi", "query": "Analyze ROI for an 80 Lakh property with 20% down payment, generating ₹25,000 monthly rent."},
    {"type": "roi", "query": "What is the cap rate for a $500k property renting for $3,000 a month? Assume 20% down."},
    {"type": "roi", "query": "Calculate investment returns for a ₹1.2 Cr apartment with ₹35k monthly rent."},
    {"type": "roi", "query": "Is a $250k condo renting for $1,800/mo a good investment? Assume $50k down payment and 7% mortgage."},
    {"type": "roi", "query": "Find the cash-on-cash return for a ₹60 Lakh house renting at ₹20,000/month."},
    {"type": "roi", "query": "What's the 5-year ROI on a $1M commercial space renting for $8k/mo with a 25% down payment?"},
    {"type": "roi", "query": "Analyze ROI for a ₹2 Cr villa with ₹50,000 monthly rent. Assume 8.5% interest and 20% down."},

    # --- 7. Market Analysis (5) ---
    {"type": "market", "query": "What are the real estate market trends in Mumbai right now?"},
    {"type": "market", "query": "Give me a market analysis for Bangalore."},
    {"type": "market", "query": "How is the real estate market in Austin, TX?"},
    {"type": "market", "query": "What are the average property prices in Pune?"},
    {"type": "market", "query": "Analyze the real estate market trends in Hyderabad."},
]

MULTI_TURN_CONVERSATIONS = [
    # Sequence 1: Search -> Market -> Mortgage
    [
        {"role": "user", "content": "I am looking for a 2 BHK apartment in Chennai under 70 Lakhs."},
        {"role": "user", "content": "How is the overall real estate market in Chennai right now?"},
        {"role": "user", "content": "If I buy a 70 Lakh property there with a 15 Lakh down payment, what would be my EMI for 20 years at 8.5%?"}
    ],
    # Sequence 2: Concept -> ROI -> Refinement
    [
        {"role": "user", "content": "What makes a good rental property investment?"},
        {"role": "user", "content": "Can you analyze the ROI if I buy a ₹1.5 Cr flat and rent it out for ₹40,000 a month?"},
        {"role": "user", "content": "What if the rent was ₹55,000 instead? How does that change the cap rate?"}
    ]
]


async def run_single_queries(agent, log_file="test_results_single.jsonl"):
    print(f"Starting {len(DATASET)} single-turn tests...")
    with open(log_file, "w") as f:
        for i, data in enumerate(DATASET):
            query = data["query"]
            qtype = data["type"]
            print(f"[{i+1}/{len(DATASET)}] Testing ({qtype}): {query}")
            
            start_time = time.time()
            try:
                # We do not pass thread_id to keep them stateless
                response = await agent.ainvoke({"messages": [HumanMessage(content=query)]})
                ai_msg = response["messages"][-1]
                
                result = {
                    "id": i+1,
                    "type": qtype,
                    "query": query,
                    "response": ai_msg.content,
                    "tools_used": [tool["name"] for tool in getattr(ai_msg, "tool_calls", [])],
                    "duration_seconds": round(time.time() - start_time, 2)
                }
                # Log success
                f.write(json.dumps(result) + "\n")
                f.flush()
            except Exception as e:
                print(f"  -> ERROR: {e}")
                error_res = {
                    "id": i+1,
                    "type": qtype,
                    "query": query,
                    "error": str(e),
                    "duration_seconds": round(time.time() - start_time, 2)
                }
                f.write(json.dumps(error_res) + "\n")
                f.flush()

async def run_multi_turn(agent, log_file="test_results_multi.jsonl"):
    print(f"\nStarting {len(MULTI_TURN_CONVERSATIONS)} multi-turn conversations...")
    with open(log_file, "w") as f:
        for seq_idx, conversation in enumerate(MULTI_TURN_CONVERSATIONS):
            thread_id = f"test_thread_{seq_idx}"
            config = {"configurable": {"thread_id": thread_id}}
            
            print(f"\n--- Conversation Sequence {seq_idx+1} ---")
            
            seq_log = {"sequence_id": seq_idx + 1, "turns": []}
            for turn_idx, msg in enumerate(conversation):
                query = msg["content"]
                print(f"  [Turn {turn_idx+1}] User: {query}")
                
                start_time = time.time()
                try:
                    response = await agent.ainvoke({"messages": [HumanMessage(content=query)]}, config=config)
                    ai_msg = response["messages"][-1]
                    print(f"  [Turn {turn_idx+1}] Assistant: <response length {len(ai_msg.content)}>")
                    
                    seq_log["turns"].append({
                        "turn": turn_idx + 1,
                        "query": query,
                        "response": ai_msg.content,
                        "tools_used": [tool["name"] for tool in getattr(ai_msg, "tool_calls", [])],
                        "duration_seconds": round(time.time() - start_time, 2)
                    })
                except Exception as e:
                    print(f"  [Turn {turn_idx+1}] ERROR: {e}")
                    seq_log["turns"].append({
                        "turn": turn_idx + 1,
                        "query": query,
                        "error": str(e)
                    })
                    break # stop this sequence
            
            f.write(json.dumps(seq_log) + "\n")
            f.flush()

async def main():
    agent = get_agent()
    # To save time and not spam MagicBricks too much sequentially, we'll run a subset if needed.
    # But since user requested at least 50 queries, we will run them all. 
    # Warning: 50 queries might take 5-10 minutes. 
    await run_single_queries(agent)
    await run_multi_turn(agent)
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
