import httpx
from app.core.config import get_settings
from typing import List, Optional
import logging

_settings = get_settings()
logger = logging.getLogger(__name__)


async def get_embedding(text: str) -> Optional[List[float]]:
    try:
        text = text.replace("\n", " ").strip()
        if not text:
            return None

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{_settings.ollama_local_url}/api/embeddings",
                json={"model": _settings.embedding_model, "prompt": text},
            )

            if response.status_code != 200:
                logger.warning(f"Embedding API error: {response.status_code}")
                return None

            data = response.json()
            return data.get("embedding")
    except httpx.TimeoutException:
        logger.warning("Embedding timeout - local Ollama may not be running")
        return None
    except Exception as e:
        logger.warning(f"Embedding error: {e}")
        return None


async def get_embeddings(texts: List[str]) -> List[Optional[List[float]]]:
    embeddings = []
    for text in texts:
        embedding = await get_embedding(text)
        embeddings.append(embedding)
    return embeddings
