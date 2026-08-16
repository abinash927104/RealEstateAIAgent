"""Vector service — ChromaDB operations for semantic search."""

import chromadb
from functools import lru_cache

from app.config import get_settings
from app.utils.embeddings import get_embedding_function, create_property_document


@lru_cache
def get_chroma_client():
    """Get a persistent ChromaDB client."""
    settings = get_settings()
    return chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)


class VectorService:
    PROPERTIES_COLLECTION = "properties"
    KNOWLEDGE_COLLECTION = "knowledge_base"

    def __init__(self):
        self.client = get_chroma_client()
        self.embedding_fn = get_embedding_function()

    def _get_collection(self, name: str):
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

    async def add_property(self, property_id: str, property_data: dict) -> None:
        """Add a property to the vector store."""
        collection = self._get_collection(self.PROPERTIES_COLLECTION)
        document = create_property_document(property_data)

        # Build metadata for filtering (ChromaDB only supports primitive types)
        metadata = {
            "city": property_data.get("city", ""),
            "state": property_data.get("state", ""),
            "price": float(property_data.get("price", 0)),
            "bedrooms": int(property_data.get("bedrooms", 0)),
            "bathrooms": int(property_data.get("bathrooms", 0)),
            "property_type": property_data.get("property_type", ""),
            "area_sqft": float(property_data.get("area_sqft", 0)),
            "status": property_data.get("status", "active"),
        }

        collection.upsert(
            documents=[document],
            metadatas=[metadata],
            ids=[property_id],
        )

    async def search_properties(
        self,
        query: str,
        n_results: int = 10,
        where: dict | None = None,
    ) -> list[dict]:
        """Semantic search for properties."""
        collection = self._get_collection(self.PROPERTIES_COLLECTION)

        kwargs = {
            "query_texts": [query],
            "n_results": n_results,
        }
        if where:
            kwargs["where"] = where

        results = collection.query(**kwargs)

        # Format results
        properties = []
        if results and results["ids"] and results["ids"][0]:
            for i, prop_id in enumerate(results["ids"][0]):
                properties.append({
                    "id": prop_id,
                    "document": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0.0,
                })

        return properties

    async def add_knowledge(self, doc_id: str, content: str, metadata: dict | None = None) -> None:
        """Add a document to the knowledge base."""
        collection = self._get_collection(self.KNOWLEDGE_COLLECTION)
        collection.upsert(
            documents=[content],
            metadatas=[metadata or {}],
            ids=[doc_id],
        )

    async def search_knowledge(self, query: str, n_results: int = 5) -> list[dict]:
        """Search the knowledge base."""
        collection = self._get_collection(self.KNOWLEDGE_COLLECTION)
        results = collection.query(query_texts=[query], n_results=n_results)

        docs = []
        if results and results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                docs.append({
                    "id": doc_id,
                    "content": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0.0,
                })

        return docs

    async def delete_property(self, property_id: str) -> None:
        """Remove a property from the vector store."""
        collection = self._get_collection(self.PROPERTIES_COLLECTION)
        collection.delete(ids=[property_id])

    def get_collection_count(self, collection_name: str) -> int:
        """Get the number of documents in a collection."""
        collection = self._get_collection(collection_name)
        return collection.count()
