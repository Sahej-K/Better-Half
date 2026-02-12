from app.config import get_settings
from typing import List
import os

settings = get_settings()

# Lazy import because either provider may be used
_openai_client = None

def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        from openai import OpenAI, AzureOpenAI
        if settings.LLM_PROVIDER.lower() == "azure":
            _openai_client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_version="2024-06-01",
            )
        else:
            _openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _openai_client

def embed_texts(texts: List[str]) -> List[List[float]]:
    client = _get_openai_client()
    if settings.LLM_PROVIDER.lower() == "azure":
        model = settings.AZURE_OPENAI_EMBED_DEPLOYMENT
    else:
        model = settings.OPENAI_EMBED_MODEL
    resp = client.embeddings.create(input=texts, model=model)
    return [d.embedding for d in resp.data]

def chat_vision_prompt(messages: List[dict], temperature: float = 0.2) -> str:
    """
    Messages = [{"role":"system"/"user"/"assistant","content":[{type:"text"/"image_url"}...]}]
    Returns assistant text.
    """
    client = _get_openai_client()
    if settings.LLM_PROVIDER.lower() == "azure":
        model = settings.AZURE_OPENAI_CHAT_DEPLOYMENT
    else:
        model = settings.OPENAI_CHAT_MODEL

    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages
    )
    return completion.choices[0].message.content

def chat_text_prompt(messages: List[dict], temperature: float = 0.3, max_tokens: int = 800) -> str:
    client = _get_openai_client()
    if settings.LLM_PROVIDER.lower() == "azure":
        model = settings.AZURE_OPENAI_CHAT_DEPLOYMENT
    else:
        model = settings.OPENAI_CHAT_MODEL

    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages
    )
    return completion.choices[0].message.content