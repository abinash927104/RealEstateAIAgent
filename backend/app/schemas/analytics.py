"""Pydantic schemas for Analytics responses."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class SearchAnalyticsResponse(BaseModel):
    id: uuid.UUID
    query_text: str | None
    query_type: str | None
    results_count: int
    response_time_ms: float
    searched_at: datetime

    model_config = {"from_attributes": True}


class DashboardAnalytics(BaseModel):
    total_searches: int
    total_conversations: int
    total_favorites: int
    avg_response_time_ms: float
    recent_searches: list[SearchAnalyticsResponse]
    popular_cities: list[dict]
    search_trend: list[dict]
