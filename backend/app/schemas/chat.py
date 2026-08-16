"""Pydantic schemas for Chat requests and responses."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.chat import MessageRole


# ── Request Schemas ─────────────────────────────────────

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: uuid.UUID | None = None


# ── Response Schemas ────────────────────────────────────

class MessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: MessageRole
    content: str
    tool_calls: dict | None = None
    tool_results: dict | None = None
    metadata_: dict | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationResponse(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}


class ConversationDetailResponse(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse]

    model_config = {"from_attributes": True}


class ChatResponse(BaseModel):
    """Full response from the AI chat endpoint."""
    conversation_id: uuid.UUID
    message: MessageResponse
    query_type: str | None = None
    tools_used: list[str] = Field(default_factory=list)
