"""LangGraph AI Agent — orchestrates tool-calling for complex real estate queries."""

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from app.config import get_settings
from app.core.agent.state import AgentState
from app.core.agent.prompts import SYSTEM_PROMPT
from app.core.tools import ALL_TOOLS


def create_agent():
    """Build and compile the LangGraph agent with tool-calling capabilities."""
    settings = get_settings()

    # LLM with tool binding
    llm = ChatOpenAI(
        model=settings.DEFAULT_LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0.3,
        streaming=True,
    )
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    # ── Graph Nodes ─────────────────────────────────────

    def agent_node(state: AgentState) -> dict:
        """Core reasoning node — decides whether to call tools or respond."""
        messages = state["messages"]

        structured_state = state.get("structured_state", {})
        state_str = "\\n".join([f"- {k}: {v}" for k, v in structured_state.items() if v is not None])
        if state_str:
            dynamic_prompt = SYSTEM_PROMPT + f"\\n\\n## Current Conversation State:\\n{state_str}\\nUse these values as defaults if the user doesn't specify them."
        else:
            dynamic_prompt = SYSTEM_PROMPT
            
        # Prepend system prompt if not already present
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=dynamic_prompt)] + messages
        elif isinstance(messages[0], SystemMessage):
            messages[0] = SystemMessage(content=dynamic_prompt)

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def should_continue(state: AgentState) -> str:
        """Routing function — check if the agent wants to call tools or finish."""
        last_message = state["messages"][-1]

        # If the LLM wants to call tools, route to the tool node
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        # Otherwise, the agent is done
        return END

    # ── Build the Graph ─────────────────────────────────

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(ALL_TOOLS))

    # Set entry point
    graph.set_entry_point("agent")

    # Add conditional edges
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})

    # After tools execute, go back to agent to process results
    graph.add_edge("tools", "agent")

    # Compile
    return graph.compile()


# Singleton agent instance
_agent = None


def get_agent():
    """Get or create the singleton agent instance."""
    global _agent
    if _agent is None:
        _agent = create_agent()
    return _agent
