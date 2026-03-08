from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    thread_id: Optional[str] = None
    use_rag: bool = True


class ChatResponse(BaseModel):
    content: str
    role: str = "assistant"


class HealthResponse(BaseModel):
    status: str
    app_name: str


class ThreadCreate(BaseModel):
    title: Optional[str] = None


class ThreadResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime


class MessageCreate(BaseModel):
    role: str
    content: str


class MessageResponse(BaseModel):
    id: str
    thread_id: str
    role: str
    content: str
    created_at: datetime


class DocumentCreate(BaseModel):
    filename: str
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None


class DocumentResponse(BaseModel):
    id: str
    user_id: str
    filename: str
    file_path: str
    file_size: Optional[int]
    mime_type: Optional[str]
    content_hash: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


class ChunkResponse(BaseModel):
    id: str
    document_id: str
    content: str
    chunk_index: int
    metadata: dict
