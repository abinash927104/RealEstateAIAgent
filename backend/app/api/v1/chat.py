"""Chat API routes — AI conversation endpoints."""

import time
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.chat import MessageRole
from app.schemas.chat import (
    ChatMessageRequest, ChatResponse, MessageResponse,
    ConversationResponse, ConversationDetailResponse,
)
from app.services.chat_service import ChatService
from app.core.query_analyzer import get_query_analyzer
from app.core.rag_pipeline import get_rag_pipeline
from app.core.agent import get_agent
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def send_message(
    data: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Send a message to the AI assistant.

    The query is classified and routed to either:
    - Direct response (greetings)
    - RAG pipeline (simple info queries)
    - AI Agent with tools (complex queries)
    """
    start_time = time.time()
    chat_service = ChatService(db)

    # Get or create conversation
    conversation = await chat_service.get_or_create_conversation(
        user_id=current_user.id,
        conversation_id=data.conversation_id,
    )

    # Save user message
    user_msg = await chat_service.add_message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=data.message,
    )

    # Classify the query
    analyzer = get_query_analyzer()
    classification = await analyzer.analyze(data.message)
    query_type = classification["query_type"]
    intent = classification["intent"]
    tools_used = []

    try:
        if query_type == "GREETING":
            # Direct greeting response
            response_text = (
                "Hello! 👋 I'm your AI Real Estate Assistant. I can help you with:\n\n"
                "🏠 **Property Search** — Find homes matching your criteria\n"
                "💰 **Mortgage Calculator** — Calculate monthly payments\n"
                "📈 **Investment Analysis** — Evaluate ROI on rental properties\n"
                "🏘️ **Market Analysis** — Get market trends and data\n\n"
                "What would you like to explore?"
            )

        elif query_type == "SIMPLE":
            # RAG pipeline for informational queries
            rag = get_rag_pipeline()
            response_text = await rag.generate(data.message)

        else:
            # Complex query → AI Agent with tools
            agent = get_agent()

            # Build conversation history for context
            history = await chat_service.get_conversation_messages(
                conversation_id=conversation.id,
                user_id=current_user.id,
                limit=20,
            )

            structured_state = {}
            # Find the last assistant message to retrieve state
            for msg in reversed(history):
                if msg.role == MessageRole.ASSISTANT and msg.metadata_:
                    structured_state = msg.metadata_.get("agent_state", {})
                    break

            messages = []
            for msg in history:
                if msg.role == MessageRole.USER:
                    messages.append(HumanMessage(content=msg.content))
                elif msg.role == MessageRole.ASSISTANT:
                    messages.append(AIMessage(content=msg.content))

            # Include the current message
            if not messages or messages[-1].content != data.message:
                messages.append(HumanMessage(content=data.message))

            # Run the agent
            result = await agent.ainvoke(
                {
                    "messages": messages,
                    "query_type": query_type,
                    "intent": intent,
                    "extracted_params": classification.get("extracted_params", {}),
                    "tool_results": [],
                    "structured_state": structured_state,
                    "final_response": None,
                }
            )

            # Extract the final response
            last_message = result["messages"][-1]
            response_text = last_message.content

            # Track which tools were used and state updates
            state_updates = {}
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tools_used.append(tc["name"])
                        if tc["name"] == "update_financial_context":
                            state_updates.update(tc.get("args", {}))
            
            # Merge state updates into structured state
            if state_updates:
                structured_state.update({k: v for k, v in state_updates.items() if v is not None})

    except Exception as e:
        logger.error(f"AI processing failed: {e}", exc_info=True)
        response_text = (
            "I apologize, but I encountered an error processing your request. "
            "Could you try rephrasing your question?"
        )
        structured_state = {}
        state_updates = {}

    # Save assistant response
    elapsed_ms = (time.time() - start_time) * 1000
    assistant_msg = await chat_service.add_message(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=response_text,
        tool_calls={"tools": tools_used} if tools_used else None,
        metadata={
            "query_type": query_type,
            "intent": intent,
            "response_time_ms": round(elapsed_ms, 2),
            "tools_used": tools_used,
            "agent_state": structured_state,
        },
    )

    # Auto-title conversation on first exchange
    if not data.conversation_id:
        title = data.message[:80] + ("..." if len(data.message) > 80 else "")
        await chat_service.update_conversation_title(conversation.id, title)

    return ChatResponse(
        conversation_id=conversation.id,
        message=MessageResponse.model_validate(assistant_msg),
        query_type=query_type,
        tools_used=tools_used,
    )


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all conversations for the current user."""
    chat_service = ChatService(db)
    results = await chat_service.list_conversations(current_user.id)
    return [
        ConversationResponse(
            id=r["conversation"].id,
            title=r["conversation"].title,
            created_at=r["conversation"].created_at,
            updated_at=r["conversation"].updated_at,
            message_count=r["message_count"],
        )
        for r in results
    ]


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a full conversation with all messages."""
    chat_service = ChatService(db)
    messages = await chat_service.get_conversation_messages(
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Get conversation metadata
    conv = await chat_service.get_or_create_conversation(
        user_id=current_user.id, conversation_id=conversation_id
    )

    return ConversationDetailResponse(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=[MessageResponse.model_validate(m) for m in messages],
    )


@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a conversation and all its messages."""
    chat_service = ChatService(db)
    deleted = await chat_service.delete_conversation(conversation_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
