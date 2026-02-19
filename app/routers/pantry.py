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
    """Return all items currently in the user's pantry."""
    res = await db.execute(select(PantryItem).order_by(PantryItem.name))
    return res.scalars().all()


@router.post("", response_model=PantryItemOut, status_code=201)
async def add_pantry_item(body: PantryItemCreate, db: AsyncSession = Depends(get_session)):
    """Add a single item to the pantry."""
    item = PantryItem(name=body.name.strip().lower(), quantity=body.quantity, notes=body.notes)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.post("/bulk", response_model=List[PantryItemOut], status_code=201)
async def add_pantry_items_bulk(items: List[PantryItemCreate], db: AsyncSession = Depends(get_session)):
    """Add multiple pantry items at once."""
    created = []
    for body in items:
        item = PantryItem(name=body.name.strip().lower(), quantity=body.quantity, notes=body.notes)
        db.add(item)
        created.append(item)
    await db.commit()
    for item in created:
        await db.refresh(item)
    return created


@router.delete("/{item_id}", status_code=204)
async def remove_pantry_item(item_id: int, db: AsyncSession = Depends(get_session)):
    """Remove a single pantry item by ID."""
    res = await db.execute(select(PantryItem).where(PantryItem.id == item_id))
    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Pantry item not found")
    await db.delete(item)
    await db.commit()


@router.delete("", status_code=204)
async def clear_pantry(db: AsyncSession = Depends(get_session)):
    """Remove all pantry items."""
    await db.execute(delete(PantryItem))
    await db.commit()
