"""Analytics API routes — user dashboard data."""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.analytics import SearchAnalytics
from app.models.chat import Conversation
from app.models.favorite import Favorite
from app.schemas.analytics import DashboardAnalytics, SearchAnalyticsResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardAnalytics)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get user dashboard analytics."""

    # Total searches
    search_count = await db.execute(
        select(func.count(SearchAnalytics.id)).where(
            SearchAnalytics.user_id == current_user.id
        )
    )
    total_searches = search_count.scalar() or 0

    # Total conversations
    conv_count = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.user_id == current_user.id
        )
    )
    total_conversations = conv_count.scalar() or 0

    # Total favorites
    fav_count = await db.execute(
        select(func.count(Favorite.id)).where(
            Favorite.user_id == current_user.id
        )
    )
    total_favorites = fav_count.scalar() or 0

    # Average response time
    avg_time = await db.execute(
        select(func.avg(SearchAnalytics.response_time_ms)).where(
            SearchAnalytics.user_id == current_user.id
        )
    )
    avg_response_time = float(avg_time.scalar() or 0)

    # Recent searches
    recent = await db.execute(
        select(SearchAnalytics)
        .where(SearchAnalytics.user_id == current_user.id)
        .order_by(desc(SearchAnalytics.searched_at))
        .limit(10)
    )
    recent_searches = [
        SearchAnalyticsResponse.model_validate(s) for s in recent.scalars().all()
    ]

    return DashboardAnalytics(
        total_searches=total_searches,
        total_conversations=total_conversations,
        total_favorites=total_favorites,
        avg_response_time_ms=round(avg_response_time, 2),
        recent_searches=recent_searches,
        popular_cities=[],
        search_trend=[],
    )
