from openai import OpenAI
from app.core.config import get_settings
from typing import List, Generator

_settings = get_settings()

api_key = _settings.ollama_api_key or "ollama"
client = OpenAI(base_url=f"{_settings.ollama_base_url}/v1", api_key=api_key)


def stream_chat_completion(messages: List[dict]) -> Generator[str, None, None]:
    response = client.chat.completions.create(
        model=_settings.ollama_model, messages=messages, stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def chat_completion(messages: List[dict]) -> str:
    response = client.chat.completions.create(
        model=_settings.ollama_model, messages=messages, stream=False
    )

    return response.choices[0].message.content
