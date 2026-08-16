"""Embedding generation helpers for ChromaDB vector store."""

from functools import lru_cache

from app.config import get_settings


@lru_cache
def get_embedding_function():
    """Get the sentence-transformer embedding function for ChromaDB."""
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    settings = get_settings()
    return SentenceTransformerEmbeddingFunction(
        model_name=settings.EMBEDDING_MODEL
    )


def create_property_document(property_data: dict) -> str:
    """
    Create a rich text document from property data for embedding.
    Combines key attributes into a narrative string for better semantic search.
    """
    parts = []

    if property_data.get("title"):
        parts.append(property_data["title"])

    # Build a descriptive sentence
    desc_parts = []
    if property_data.get("bedrooms"):
        desc_parts.append(f"{property_data['bedrooms']}-bedroom")
    if property_data.get("bathrooms"):
        desc_parts.append(f"{property_data['bathrooms']}-bathroom")
    if property_data.get("property_type"):
        desc_parts.append(property_data["property_type"])
    if desc_parts:
        parts.append(" ".join(desc_parts))

    if property_data.get("city") and property_data.get("state"):
        parts.append(f"located in {property_data['city']}, {property_data['state']}")

    if property_data.get("price"):
        parts.append(f"priced at ${property_data['price']:,.0f}")

    if property_data.get("area_sqft"):
        parts.append(f"{property_data['area_sqft']:,.0f} square feet")

    if property_data.get("description"):
        parts.append(property_data["description"])

    # Include features
    features = property_data.get("features", {})
    if isinstance(features, dict):
        feature_list = [k for k, v in features.items() if v]
        if feature_list:
            parts.append(f"Features: {', '.join(feature_list)}")

    return ". ".join(parts)
