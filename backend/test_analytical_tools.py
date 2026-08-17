import asyncio
from app.core.agent.graph import get_agent
from langchain_core.messages import HumanMessage

async def main():
    agent = get_agent()
    print("\n--- Testing Mortgage Calculator ---")
    res1 = await agent.ainvoke({"messages": [HumanMessage(content="Calculate EMI for a ₹1.5 Cr home with ₹30L down payment at 8.5% interest over 20 years")]})
    print(res1["messages"][-1].content)

    print("\n--- Testing Market Analysis ---")
    res2 = await agent.ainvoke({"messages": [HumanMessage(content="What are the real estate market trends in Mumbai right now?")]})
    print(res2["messages"][-1].content)

    print("\n--- Testing ROI Analysis ---")
    res3 = await agent.ainvoke({"messages": [HumanMessage(content="Analyze ROI for a 80 Lakh property with 20% down payment, generating ₹25,000 monthly rent")]})
    print(res3["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
