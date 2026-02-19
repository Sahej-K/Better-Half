from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.deps import get_session
from app.models import PantryItem, UserPreference
from app.schemas import SuggestRequest, SuggestResponse
from app.services.recipe_suggester import suggest_recipes
from app.services.utils import csv_to_list

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/suggest", response_model=SuggestResponse)
async def suggest(body: SuggestRequest, db: AsyncSession = Depends(get_session)):
    # 1. Get pantry items
    if body.pantry_override:
        pantry_names = body.pantry_override
    else:
        result = await db.execute(select(PantryItem))
        pantry_names = [item.name for item in result.scalars().all()]

    # 2. Get user preferences
    res = await db.execute(select(UserPreference).limit(1))
    pref = res.scalar_one_or_none()

    diets = csv_to_list(pref.diets) if pref else []
    allergies = csv_to_list(pref.allergies) if pref else []
    disliked = csv_to_list(pref.disliked) if pref else []
    preferred_cuisines = csv_to_list(pref.preferred_cuisines) if pref else []

    # 3. Generate suggestions
    recipes = suggest_recipes(
        pantry_items=pantry_names,
        diets=diets,
        allergies=allergies,
        disliked=disliked,
        preferred_cuisines=preferred_cuisines,
        cuisine_filter=body.cuisine,
        servings=body.servings or 2,
    )

    return SuggestResponse(recipes=recipes)
