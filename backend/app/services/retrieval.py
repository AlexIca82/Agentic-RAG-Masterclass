from app.core.supabase import supabase_admin
from app.services.embeddings import get_embedding
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


async def search_similar_chunks(
    user_id: str, query: str, top_k: int = 5, threshold: float = 0.3
) -> List[dict]:
    query_embedding = await get_embedding(query)
    if not query_embedding:
        logger.error("Failed to get query embedding")
        return []

    try:
        result = supabase_admin.rpc(
            "search_chunks",
            {
                "query_embedding": query_embedding,
                "query_user_id": user_id,
                "match_threshold": threshold,
                "match_count": top_k,
            },
        ).execute()

        return result.data or []
    except Exception as e:
        logger.error(f"Search error: {e}")
        return []


async def get_context_for_query(user_id: str, query: str, top_k: int = 5) -> str:
    chunks = await search_similar_chunks(user_id, query, top_k)

    if not chunks:
        return ""

    contexts = []
    for chunk in chunks:
        contexts.append(chunk.get("content", ""))

    return "\n\n---\n\n".join(contexts)
