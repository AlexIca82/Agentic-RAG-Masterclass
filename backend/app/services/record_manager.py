import hashlib
from typing import Optional, Tuple
from app.core.supabase import supabase_admin
import logging

logger = logging.getLogger(__name__)


def compute_content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


async def check_existing_document(user_id: str, content_hash: str) -> Optional[dict]:
    try:
        result = (
            supabase_admin.table("documents")
            .select("*")
            .eq("user_id", user_id)
            .eq("content_hash", content_hash)
            .execute()
        )

        if result.data:
            return result.data[0]
        return None
    except Exception as e:
        logger.error(f"Error checking existing document: {e}")
        return None


async def delete_document_chunks(document_id: str) -> bool:
    try:
        supabase_admin.table("chunks").delete().eq("document_id", document_id).execute()
        return True
    except Exception as e:
        logger.error(f"Error deleting chunks: {e}")
        return False


async def update_document_status(
    document_id: str, status: str, error_message: Optional[str] = None
) -> bool:
    try:
        update_data = {"status": status}
        if error_message:
            update_data["error_message"] = error_message

        supabase_admin.table("documents").update(update_data).eq(
            "id", document_id
        ).execute()
        return True
    except Exception as e:
        logger.error(f"Error updating document status: {e}")
        return False
