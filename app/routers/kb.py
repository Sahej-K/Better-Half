from fastapi import APIRouter
from app.services.rag import get_collection

router = APIRouter(prefix="/kb", tags=["kb"])

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
@router.get("/stats")
def kb_stats():
    col = get_collection()
    count = col.count()
    return {"collection": "recipes", "count": count}
