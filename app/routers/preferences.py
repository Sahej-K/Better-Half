from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
from app.deps import get_session
from app.models import UserPreference
from app.schemas import PreferenceUpdate, PreferenceOut
from app.services.utils import list_to_csv, csv_to_list

router = APIRouter(prefix="/preferences", tags=["preferences"])

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
@router.get("", response_model=PreferenceOut)
async def get_preferences(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(UserPreference).limit(1))
    pref = res.scalar_one_or_none()
    if not pref:
        pref = UserPreference()
        db.add(pref)
        await db.commit()
        await db.refresh(pref)
    return PreferenceOut(
        diets=csv_to_list(pref.diets),
        allergies=csv_to_list(pref.allergies),
        disliked=csv_to_list(pref.disliked),
<<<<<<< HEAD
        preferred_cuisines=csv_to_list(pref.preferred_cuisines),
    )


@router.put("", response_model=PreferenceOut)
async def update_preferences(
    body: PreferenceUpdate, db: AsyncSession = Depends(get_session)
):
=======
        preferred_cuisines=csv_to_list(pref.preferred_cuisines)
    )

@router.put("", response_model=PreferenceOut)
async def update_preferences(body: PreferenceUpdate, db: AsyncSession = Depends(get_session)):
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
    res = await db.execute(select(UserPreference).limit(1))
    pref = res.scalar_one_or_none()
    if not pref:
        pref = UserPreference()
        db.add(pref)

    if body.diets is not None:
        pref.diets = list_to_csv(body.diets)
    if body.allergies is not None:
        pref.allergies = list_to_csv(body.allergies)
    if body.disliked is not None:
        pref.disliked = list_to_csv(body.disliked)
    if body.preferred_cuisines is not None:
        pref.preferred_cuisines = list_to_csv(body.preferred_cuisines)

    await db.commit()
    await db.refresh(pref)
    return PreferenceOut(
        diets=csv_to_list(pref.diets),
        allergies=csv_to_list(pref.allergies),
        disliked=csv_to_list(pref.disliked),
<<<<<<< HEAD
        preferred_cuisines=csv_to_list(pref.preferred_cuisines),
=======
        preferred_cuisines=csv_to_list(pref.preferred_cuisines)
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
    )
