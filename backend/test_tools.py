import asyncio
from app.core.agent.graph import get_agent
from langchain_core.messages import HumanMessage

async def main():
    agent = get_agent()
    # Test Mortgage Calculator
    res = await agent.ainvoke({"messages": [HumanMessage(content="Calculate EMI for a ₹1.5 Cr home with ₹30L down payment at 8.5% interest over 20 years")]})
    
    last_msg = res["messages"][-1]
    print("Mortgage test tools called:", getattr(last_msg, "tool_calls", None) if last_msg.role == "assistant" else "None")

    # Test Market Analysis
    res2 = await agent.ainvoke({"messages": [HumanMessage(content="What are the real estate market trends in Bangalore right now?")]})
    last_msg2 = res2["messages"][-1]
    print("Market test tools called:", getattr(last_msg2, "tool_calls", None) if last_msg2.role == "assistant" else "None")

asyncio.run(main())
