from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
from app.deps import get_session
from app.models import PantryItem
from app.schemas import PantryItemCreate, PantryItemOut

router = APIRouter(prefix="/pantry", tags=["pantry"])


@router.get("", response_model=List[PantryItemOut])
async def list_pantry(db: AsyncSession = Depends(get_session)):
<<<<<<< HEAD
    result = await db.execute(select(PantryItem).order_by(PantryItem.name))
    items = result.scalars().all()
    return items
=======
    """Return all items currently in the user's pantry."""
    res = await db.execute(select(PantryItem).order_by(PantryItem.name))
    return res.scalars().all()
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0


@router.post("", response_model=PantryItemOut, status_code=201)
async def add_pantry_item(body: PantryItemCreate, db: AsyncSession = Depends(get_session)):
<<<<<<< HEAD
=======
    """Add a single item to the pantry."""
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
    item = PantryItem(name=body.name.strip().lower(), quantity=body.quantity, notes=body.notes)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


<<<<<<< HEAD
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
=======
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
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
    if not item:
        raise HTTPException(status_code=404, detail="Pantry item not found")
    await db.delete(item)
    await db.commit()


@router.delete("", status_code=204)
async def clear_pantry(db: AsyncSession = Depends(get_session)):
<<<<<<< HEAD
=======
    """Remove all pantry items."""
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
    await db.execute(delete(PantryItem))
    await db.commit()
