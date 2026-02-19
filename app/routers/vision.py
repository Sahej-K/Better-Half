from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
<<<<<<< HEAD
=======
from sqlalchemy import select
from typing import List
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
from app.deps import get_session
from app.schemas import VisionIn, VisionOut
from app.models import PantryItem
from app.services.image import extract_ingredients_from_image_url

router = APIRouter(prefix="/vision", tags=["vision"])

<<<<<<< HEAD

@router.post("/pantry", response_model=VisionOut)
async def ingest_pantry_from_image(
    body: VisionIn, db: AsyncSession = Depends(get_session)
):
=======
@router.post("/pantry", response_model=VisionOut)
async def ingest_pantry_from_image(body: VisionIn, db: AsyncSession = Depends(get_session)):
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
    if not body.image_url:
        raise HTTPException(status_code=400, detail="Provide image_url")
    items = extract_ingredients_from_image_url(body.image_url)
    added = 0
    if body.add_to_pantry:
<<<<<<< HEAD
        for name in items:
            rec = PantryItem(name=name)
=======
        for i in items:
            rec = PantryItem(name=i)
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
            db.add(rec)
            added += 1
        await db.commit()
    return {"detected_items": items, "added_count": added}
