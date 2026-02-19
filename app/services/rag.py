import re
from typing import List, Dict, Any
import chromadb
from app.config import get_settings
from app.services.llm import embed_texts

settings = get_settings()

_client = None
_collection = None


def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.VECTOR_DB_DIR)
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = _get_client()
        _collection = client.get_or_create_collection(
            name="recipes",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def normalize_ingredient(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9 ]+", "", s).strip().lower()


def upsert_recipe_docs(docs: List[Dict[str, Any]]):
    """
    docs: list of dicts with keys:
      id, title, cuisine, tags[], ingredients[], content, path
    """
    col = get_collection()
    ids = [d["id"] for d in docs]
    metadatas = [
        {
            "title": d.get("title", ""),
            "cuisine": d.get("cuisine", ""),
            "tags": ",".join(d.get("tags", [])),
            "path": d.get("path", ""),
        }
        for d in docs
    ]
    documents = [d["content"] for d in docs]
    embeddings = embed_texts(documents)
    col.upsert(ids=ids, metadatas=metadatas, documents=documents, embeddings=embeddings)


def search(query: str, k: int = 5, cuisine: str | None = None) -> List[Dict[str, Any]]:
    col = get_collection()
    query_emb = embed_texts([query])
    where_filter = {"cuisine": cuisine} if cuisine else None
    res = col.query(
        query_embeddings=query_emb,
        n_results=k,
        where=where_filter,
    )
    out = []
    for i in range(len(res["ids"][0])):
        out.append(
            {
                "id": res["ids"][0][i],
                "document": res["documents"][0][i],
                "metadata": res["metadatas"][0][i],
                "distance": res["distances"][0][i] if "distances" in res else None,
            }
        )
    return out
