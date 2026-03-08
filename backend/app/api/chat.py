from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Header
from fastapi.responses import StreamingResponse
from typing import List
from app.models.chat import (
    ChatRequest,
    HealthResponse,
    ThreadCreate,
    ThreadResponse,
    MessageResponse,
    DocumentResponse,
)
from app.services.llm import stream_chat_completion
from app.services.chunking import chunk_text
from app.services.embeddings import get_embedding
from app.services.retrieval import get_context_for_query
from app.core.config import get_settings
from app.core.supabase import supabase_admin
import json
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


def get_user_id(authorization: str = Header(None)) -> str:
    if not authorization:
        return "dev-user"
    if authorization.startswith("Bearer "):
        token = authorization[7:]
        try:
            result = supabase_admin.auth.get_user(token)
            return result.user.id
        except Exception:
            return "dev-user"
    return "dev-user"


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", app_name=settings.app_name)


@router.post("/chat")
async def chat(request: ChatRequest, user_id: str = Depends(get_user_id)):
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]

    if request.use_rag and messages:
        last_message = messages[-1]["content"]
        context = await get_context_for_query(user_id, last_message)

        if context:
            system_message = {
                "role": "system",
                "content": f"Use the following context to answer the question. If the context is not relevant, ignore it.\n\nContext:\n{context}",
            }
            messages = [system_message] + messages

    def generate():
        for chunk in stream_chat_completion(messages):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.post("/threads", response_model=ThreadResponse)
async def create_thread(thread: ThreadCreate, user_id: str = Depends(get_user_id)):
    result = (
        supabase_admin.table("threads")
        .insert({"user_id": user_id, "title": thread.title})
        .execute()
    )
    return result.data[0]


@router.get("/threads", response_model=List[ThreadResponse])
async def list_threads(user_id: str = Depends(get_user_id)):
    result = (
        supabase_admin.table("threads")
        .select("*")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .execute()
    )
    return result.data


@router.get("/threads/{thread_id}/messages", response_model=List[MessageResponse])
async def get_thread_messages(thread_id: str, user_id: str = Depends(get_user_id)):
    thread = (
        supabase_admin.table("threads")
        .select("*")
        .eq("id", thread_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not thread.data:
        raise HTTPException(status_code=404, detail="Thread not found")

    result = (
        supabase_admin.table("messages")
        .select("*")
        .eq("thread_id", thread_id)
        .order("created_at")
        .execute()
    )
    return result.data


@router.post("/threads/{thread_id}/messages", response_model=MessageResponse)
async def add_message(
    thread_id: str, role: str, content: str, user_id: str = Depends(get_user_id)
):
    thread = (
        supabase_admin.table("threads")
        .select("*")
        .eq("id", thread_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not thread.data:
        raise HTTPException(status_code=404, detail="Thread not found")

    result = (
        supabase_admin.table("messages")
        .insert(
            {
                "thread_id": thread_id,
                "user_id": user_id,
                "role": role,
                "content": content,
            }
        )
        .execute()
    )
    return result.data[0]


@router.post("/documents", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...), user_id: str = Depends(get_user_id)
):
    file_content = await file.read()
    file_path = f"{user_id}/{uuid.uuid4()}_{file.filename}"

    supabase_admin.storage.from_("documents").upload(file_path, file_content)

    doc_result = (
        supabase_admin.table("documents")
        .insert(
            {
                "user_id": user_id,
                "filename": file.filename,
                "file_path": file_path,
                "file_size": len(file_content),
                "mime_type": file.content_type,
                "status": "processing",
            }
        )
        .execute()
    )

    document = doc_result.data[0]

    try:
        text = file_content.decode("utf-8")
        chunks = chunk_text(text)

        for chunk in chunks:
            embedding = await get_embedding(chunk["content"])
            if embedding:
                supabase_admin.table("chunks").insert(
                    {
                        "document_id": document["id"],
                        "user_id": user_id,
                        "content": chunk["content"],
                        "embedding": embedding,
                        "chunk_index": chunk["chunk_index"],
                        "metadata": chunk["metadata"],
                    }
                ).execute()

        supabase_admin.table("documents").update({"status": "completed"}).eq(
            "id", document["id"]
        ).execute()
    except Exception as e:
        logger.error(f"Document processing error: {e}")
        supabase_admin.table("documents").update(
            {"status": "failed", "error_message": str(e)}
        ).eq("id", document["id"]).execute()

    result = (
        supabase_admin.table("documents").select("*").eq("id", document["id"]).execute()
    )
    return result.data[0]


@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents(user_id: str = Depends(get_user_id)):
    result = (
        supabase_admin.table("documents")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str, user_id: str = Depends(get_user_id)):
    doc = (
        supabase_admin.table("documents")
        .select("*")
        .eq("id", document_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not doc.data:
        raise HTTPException(status_code=404, detail="Document not found")

    supabase_admin.storage.from_("documents").remove([doc.data[0]["file_path"]])
    supabase_admin.table("documents").delete().eq("id", document_id).execute()

    return {"status": "deleted"}
