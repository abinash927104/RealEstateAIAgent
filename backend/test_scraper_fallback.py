import asyncio
from app.core.agent.graph import get_agent
from langchain_core.messages import HumanMessage

async def main():
    agent = get_agent()
    print("\n--- Testing Market Analysis (Kolkata) ---")
    res = await agent.ainvoke({"messages": [HumanMessage(content="What are the market trends in Kolkata?")]})
    print(res["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
