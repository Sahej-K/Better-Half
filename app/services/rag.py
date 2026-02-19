<<<<<<< HEAD
import re
from typing import List, Dict, Any
import chromadb
=======
import os
import glob
import re
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
from app.config import get_settings
from app.services.llm import embed_texts

settings = get_settings()

_client = None
_collection = None

<<<<<<< HEAD

def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.VECTOR_DB_DIR)
    return _client


=======
def _get_client():
    global _client
    if _client is None:
        _client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.VECTOR_DB_DIR,
                is_persistent=True
            )
        )
    return _client

>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
def get_collection():
    global _collection
    if _collection is None:
        client = _get_client()
        _collection = client.get_or_create_collection(
            name="recipes",
<<<<<<< HEAD
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
=======
            metadata={"hnsw:space": "cosine"}
        )
    return _collection

def normalize_ingredient(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9 ]+", "", s).strip().lower()

def upsert_recipe_docs(docs: List[Dict[str, Any]]):
    """
    docs: list of {"id", "title", "cuisine", "tags":[], "ingredients":[str], "content":str, "path": str}
    """
    col = get_collection()
    ids = [d["id"] for d in docs]
    metadatas = [{
        "title": d.get("title"),
        "cuisine": d.get("cuisine"),
        "tags": ",".join(d.get("tags", [])),
        "ingredients": ",".join(normalize_ingredient(x) for x in d.get("ingredients", [])),
        "path": d.get("path", ""),
    } for d in docs]
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
    documents = [d["content"] for d in docs]
    embeddings = embed_texts(documents)
    col.upsert(ids=ids, metadatas=metadatas, documents=documents, embeddings=embeddings)

<<<<<<< HEAD

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
=======
def search(query: str, k: int = 5, cuisine: str | None = None) -> List[Dict[str, Any]]:
    col = get_collection()
    res = col.query(
        query_embeddings=embed_texts([query]),
        n_results=k,
        where={"cuisine": cuisine} if cuisine else None
    )
    out = []
    for i in range(len(res["ids"][0])):
        out.append({
            "id": res["ids"][0][i],
            "document": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
            "distance": res["distances"][0][i] if "distances" in res else None
        })
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
    return out
