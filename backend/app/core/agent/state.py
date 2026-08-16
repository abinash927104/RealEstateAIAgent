"""Agent state schema for LangGraph."""

from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State that flows through the LangGraph agent."""
    # Chat messages (user + assistant + tool)
    messages: Annotated[list, add_messages]
    # Classified query type
    query_type: str
    # Detected intent
    intent: str
    # Extracted parameters from the query
    extracted_params: dict
    # Results from tool executions
    tool_results: list[dict]
    # Final response text
    final_response: str | None
