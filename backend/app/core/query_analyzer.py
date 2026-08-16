"""Query Analyzer — classifies incoming queries and routes to RAG or Agent."""

import json
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import get_settings
from app.core.agent.prompts import QUERY_CLASSIFIER_PROMPT

logger = logging.getLogger(__name__)


class QueryAnalyzer:
    """Classifies user queries to route them to the appropriate pipeline."""

    def __init__(self):
        settings = get_settings()
        # Use a cheaper/faster model for classification
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.OPENAI_API_KEY,
            temperature=0,
        )

    async def analyze(self, query: str) -> dict:
        """
        Analyze a user query and return classification results.

        Returns:
            dict with keys: query_type, intent, extracted_params, reasoning
        """
        try:
            messages = [
                SystemMessage(content=QUERY_CLASSIFIER_PROMPT),
                HumanMessage(content=query),
            ]

            response = await self.llm.ainvoke(messages)
            content = response.content.strip()

            # Parse JSON from response
            # Handle markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)

            # Validate required fields
            result.setdefault("query_type", "SIMPLE")
            result.setdefault("intent", "general_info")
            result.setdefault("extracted_params", {})
            result.setdefault("reasoning", "")

            logger.info(
                f"Query classified: type={result['query_type']}, "
                f"intent={result['intent']}, "
                f"reasoning={result['reasoning']}"
            )

            return result

        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Query analysis failed: {e}. Defaulting to COMPLEX.")
            return {
                "query_type": "COMPLEX",
                "intent": "general_info",
                "extracted_params": {},
                "reasoning": f"Classification failed: {str(e)}. Routing to agent for safety.",
            }


# Singleton
_analyzer = None


def get_query_analyzer() -> QueryAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = QueryAnalyzer()
    return _analyzer
