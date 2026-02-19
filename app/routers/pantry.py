from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from app.deps import get_session
from app.models import PantryItem
from app.schemas import PantryItemCreate, PantryItemOut

router = APIRouter(prefix="/pantry", tags=["pantry"])


@router.get("", response_model=List[PantryItemOut])
async def list_pantry(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(PantryItem).order_by(PantryItem.name))
    items = result.scalars().all()
    return items


@router.post("", response_model=PantryItemOut, status_code=201)
async def add_pantry_item(body: PantryItemCreate, db: AsyncSession = Depends(get_session)):
    item = PantryItem(name=body.name.strip().lower(), quantity=body.quantity, notes=body.notes)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/{item_id}", response_model=PantryItemOut)
async def update_pantry_item(
    item_id: int, body: PantryItemCreate, db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(PantryItem).where(PantryItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Pantry item not found")
    item.name = body.name.strip().lower()
    item.quantity = body.quantity
    item.notes = body.notes
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_pantry_item(item_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(PantryItem).where(PantryItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Pantry item not found")
    await db.delete(item)
    await db.commit()


@router.delete("", status_code=204)
async def clear_pantry(db: AsyncSession = Depends(get_session)):
    await db.execute(delete(PantryItem))
    await db.commit()
