"""RAG Pipeline — retrieval-augmented generation for simple/informational queries."""

import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import get_settings
from app.services.vector_service import VectorService

logger = logging.getLogger(__name__)

RAG_SYSTEM_PROMPT = """You are a knowledgeable real estate assistant. Answer the user's question 
using ONLY the provided context. If the context doesn't contain enough information, say so honestly.

## Context from knowledge base:
{context}

## Rules:
- Answer based on the provided context
- If you cite specific data, mention the source
- Keep answers concise and well-formatted
- If unsure, suggest the user ask a more specific question or use the chat for property searches
"""


class RAGPipeline:
    """Retrieval-Augmented Generation for informational real estate queries."""

    def __init__(self):
        settings = get_settings()
        self.llm = ChatOpenAI(
            model=settings.DEFAULT_LLM_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.3,
        )
        self.vector_service = VectorService()

    async def generate(self, query: str) -> str:
        """
        Retrieve relevant documents and generate a grounded response.
        """
        # Retrieve from both knowledge base and properties
        knowledge_results = await self.vector_service.search_knowledge(query, n_results=5)
        property_results = await self.vector_service.search_properties(query, n_results=3)

        # Build context
        context_parts = []

        if knowledge_results:
            context_parts.append("**Knowledge Base:**")
            for doc in knowledge_results:
                context_parts.append(f"- {doc['content']}")

        if property_results:
            context_parts.append("\n**Related Properties:**")
            for prop in property_results:
                context_parts.append(f"- {prop['document']}")

        context = "\n".join(context_parts) if context_parts else "No relevant context found."

        # Generate response
        messages = [
            SystemMessage(content=RAG_SYSTEM_PROMPT.format(context=context)),
            HumanMessage(content=query),
        ]

        response = await self.llm.ainvoke(messages)
        return response.content


# Singleton
_rag = None


def get_rag_pipeline() -> RAGPipeline:
    global _rag
    if _rag is None:
        _rag = RAGPipeline()
    return _rag
