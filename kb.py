from fastapi import APIRouter
from app.services.rag import get_collection

router = APIRouter(prefix="/kb", tags=["kb"])

@router.get("/stats")
def kb_stats():
    col = get_collection()
    count = col.count()
    return {"collection": "recipes", "count": count}