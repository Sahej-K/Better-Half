from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.deps import get_session
from app.schemas import VisionIn, VisionOut
from app.models import PantryItem
from app.services.image import extract_ingredients_from_image_url

router = APIRouter(prefix="/vision", tags=["vision"])

@router.post("/pantry", response_model=VisionOut)
async def ingest_pantry_from_image(body: VisionIn, db: AsyncSession = Depends(get_session)):
    if not body.image_url:
        raise HTTPException(status_code=400, detail="Provide image_url")
    items = extract_ingredients_from_image_url(body.image_url)
    added = 0
    if body.add_to_pantry:
        for i in items:
            rec = PantryItem(name=i)
            db.add(rec)
            added += 1
        await db.commit()
    return {"detected_items": items, "added_count": added}
