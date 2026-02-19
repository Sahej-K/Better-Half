<<<<<<< HEAD
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.deps import get_session
from app.models import PantryItem, UserPreference
from app.schemas import SuggestRequest, SuggestResponse
from app.services.recipe_suggester import suggest_recipes
=======
import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.deps import get_session
from app.models import PantryItem, UserPreference
from app.schemas import SuggestRequest, SuggestResponse, SuggestedRecipe, MissingItem
from app.services.rag import search as rag_search, normalize_ingredient
from app.services.llm import chat_text_prompt
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
from app.services.utils import csv_to_list

router = APIRouter(prefix="/recipes", tags=["recipes"])

<<<<<<< HEAD

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
=======
SUGGEST_SYSTEM = """\
You are ChefGenie, an expert chef AI. Given:
- The user's pantry ingredients
- Their dietary restrictions, allergies, and disliked ingredients
- Candidate recipes retrieved from a knowledge base

Your job: suggest up to 3 recipes the user can make. For each recipe, output a JSON object with:
  title, cuisine, ingredients (list of strings), missing (list of {name, suggested_quantity}),
  steps (list of strings), citations (list of KB doc ids used), score (0-1 float, higher=better match).

Return ONLY a JSON array of recipe objects. No markdown, no explanation.
If allow_missing is false, only suggest recipes where the user has ALL ingredients.
"""


def _build_user_prompt(
    pantry: List[str],
    prefs: dict,
    candidates: list,
    cuisine: str | None,
    servings: int,
    allow_missing: bool,
) -> str:
    parts = [
        f"Pantry ingredients: {', '.join(pantry) if pantry else '(empty)'}",
        f"Dietary restrictions: {', '.join(prefs.get('diets', [])) or 'none'}",
        f"Allergies: {', '.join(prefs.get('allergies', [])) or 'none'}",
        f"Disliked ingredients: {', '.join(prefs.get('disliked', [])) or 'none'}",
        f"Preferred cuisines: {', '.join(prefs.get('preferred_cuisines', [])) or 'any'}",
        f"Requested cuisine filter: {cuisine or 'any'}",
        f"Servings: {servings}",
        f"Allow recipes with missing ingredients: {allow_missing}",
        "",
        "--- Candidate recipes from knowledge base ---",
    ]
    for c in candidates:
        meta = c.get("metadata", {})
        parts.append(
            f"[{c['id']}] {meta.get('title', 'Untitled')} (cuisine: {meta.get('cuisine', '?')}, "
            f"ingredients: {meta.get('ingredients', '')})\n{c['document'][:500]}"
        )
    parts.append("\nReturn a JSON array of up to 3 suggested recipes.")
    return "\n".join(parts)


def _parse_recipes(raw: str) -> List[SuggestedRecipe]:
    """Best-effort parse of LLM JSON response."""
    # Strip markdown fences if present
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        arr = json.loads(text)
    except json.JSONDecodeError:
        return []

    recipes = []
    for item in arr:
        missing = []
        for m in item.get("missing", []):
            if isinstance(m, dict):
                missing.append(MissingItem(name=m.get("name", ""), suggested_quantity=m.get("suggested_quantity")))
            elif isinstance(m, str):
                missing.append(MissingItem(name=m))
        recipes.append(
            SuggestedRecipe(
                title=item.get("title", "Untitled"),
                cuisine=item.get("cuisine"),
                ingredients=item.get("ingredients", []),
                missing=missing,
                steps=item.get("steps", []),
                citations=item.get("citations", []),
                score=float(item.get("score", 0.5)),
            )
        )
    return recipes


@router.post("/suggest", response_model=SuggestResponse)
async def suggest_recipes(body: SuggestRequest, db: AsyncSession = Depends(get_session)):
    # 1. Gather pantry
    if body.pantry_override:
        pantry = [normalize_ingredient(i) for i in body.pantry_override]
    else:
        res = await db.execute(select(PantryItem))
        pantry = [normalize_ingredient(item.name) for item in res.scalars().all()]

    # 2. Gather preferences
    pref_row = (await db.execute(select(UserPreference).limit(1))).scalar_one_or_none()
    prefs = {}
    if pref_row:
        prefs = {
            "diets": csv_to_list(pref_row.diets),
            "allergies": csv_to_list(pref_row.allergies),
            "disliked": csv_to_list(pref_row.disliked),
            "preferred_cuisines": csv_to_list(pref_row.preferred_cuisines),
        }

    # 3. RAG search
    query = " ".join(pantry[:30]) if pantry else "popular easy recipe"
    candidates = rag_search(query, k=5, cuisine=body.cuisine)

    # 4. LLM generation
    user_prompt = _build_user_prompt(
        pantry, prefs, candidates,
        cuisine=body.cuisine,
        servings=body.servings or 2,
        allow_missing=body.allow_missing,
    )
    messages = [
        {"role": "system", "content": SUGGEST_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]
    raw = chat_text_prompt(messages, temperature=0.4, max_tokens=2000)
    recipes = _parse_recipes(raw)
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0

    return SuggestResponse(recipes=recipes)
