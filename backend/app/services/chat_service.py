"""Chat service — conversation and message persistence."""

import uuid

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chat import Conversation, Message, MessageRole


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_conversation(
        self, user_id: uuid.UUID, conversation_id: uuid.UUID | None = None
    ) -> Conversation:
        if conversation_id:
            result = await self.db.execute(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id,
                )
            )
            conv = result.scalar_one_or_none()
            if conv:
                return conv

        # Create new conversation
        conv = Conversation(user_id=user_id)
        self.db.add(conv)
        await self.db.flush()
        await self.db.refresh(conv)
        return conv

    async def add_message(
        self,
        conversation_id: uuid.UUID,
        role: MessageRole,
        content: str,
        tool_calls: dict | None = None,
        tool_results: dict | None = None,
        metadata: dict | None = None,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_results=tool_results,
            metadata_=metadata,
        )
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def get_conversation_messages(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID, limit: int = 50
    ) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .join(Conversation)
            .where(
                Message.conversation_id == conversation_id,
                Conversation.user_id == user_id,
            )
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def list_conversations(self, user_id: uuid.UUID) -> list[dict]:
        result = await self.db.execute(
            select(
                Conversation,
                func.count(Message.id).label("message_count"),
            )
            .outerjoin(Message)
            .where(Conversation.user_id == user_id)
            .group_by(Conversation.id)
            .order_by(desc(Conversation.updated_at))
        )
        rows = result.all()
        return [
            {
                "conversation": row[0],
                "message_count": row[1],
            }
            for row in rows
        ]

    async def update_conversation_title(
        self, conversation_id: uuid.UUID, title: str
    ) -> None:
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conv = result.scalar_one_or_none()
        if conv:
            conv.title = title
            await self.db.flush()

    async def delete_conversation(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> bool:
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )
        conv = result.scalar_one_or_none()
        if not conv:
            return False
        await self.db.delete(conv)
        await self.db.flush()
        return True
