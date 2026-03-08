from app.core.config import get_settings
from typing import List

_settings = get_settings()


def chunk_text(
    text: str, chunk_size: int = None, chunk_overlap: int = None
) -> List[dict]:
    chunk_size = chunk_size or _settings.chunk_size
    chunk_overlap = chunk_overlap or _settings.chunk_overlap

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk_content = text[start:end]

        if chunk_content.strip():
            chunks.append(
                {
                    "content": chunk_content,
                    "chunk_index": chunk_index,
                    "metadata": {"start_char": start, "end_char": min(end, len(text))},
                }
            )
            chunk_index += 1

        start = end - chunk_overlap
        if start <= chunks[-1]["metadata"]["start_char"] if chunks else 0:
            start = end

    return chunks


def chunk_by_paragraph(text: str, max_chunk_size: int = None) -> List[dict]:
    max_chunk_size = max_chunk_size or _settings.chunk_size

    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    chunk_index = 0
    start_char = 0

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + para
        else:
            if current_chunk.strip():
                chunks.append(
                    {
                        "content": current_chunk.strip(),
                        "chunk_index": chunk_index,
                        "metadata": {
                            "start_char": start_char,
                            "end_char": start_char + len(current_chunk),
                        },
                    }
                )
                chunk_index += 1
            current_chunk = para
            start_char = text.find(para, start_char + len(current_chunk))

    if current_chunk.strip():
        chunks.append(
            {
                "content": current_chunk.strip(),
                "chunk_index": chunk_index,
                "metadata": {
                    "start_char": start_char,
                    "end_char": start_char + len(current_chunk),
                },
            }
        )

    return chunks
