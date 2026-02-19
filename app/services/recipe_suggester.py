"""
Recipe Suggestion Engine
========================
Combines pantry items + user preferences + RAG knowledge base + LLM
to generate personalised recipe suggestions.
"""

import json
import re
from typing import List, Optional

from app.services.llm import chat_text_prompt
from app.services.rag import search as rag_search
from app.schemas import SuggestedRecipe, MissingItem


SYSTEM_PROMPT = """\
You are ChefGenie, an expert chef AI assistant. Your job is to suggest recipes
that the user can make with the ingredients they have on hand.

Rules:
- Respect all dietary restrictions and allergies — NEVER include allergens.
- Prefer recipes that use more of the user's available ingredients.
- For each recipe, list ALL ingredients (including ones the user is missing).
- Clearly mark which ingredients the user is missing.
- Give practical, numbered cooking steps.
- Return your answer as a JSON array of recipe objects.

Each recipe object must have EXACTLY these fields:
{
  "title": "Recipe Title",
  "cuisine": "Italian",
  "ingredients": ["ingredient 1", "ingredient 2"],
  "missing": [{"name": "butter", "suggested_quantity": "2 tbsp"}],
  "steps": ["Step 1: ...", "Step 2: ..."],
  "citations": [],
  "score": 0.85
}

The "score" is 0.0-1.0 representing how well the recipe matches the user's pantry.
Higher score = fewer missing ingredients. Return 2-4 recipes, ordered by score descending.
Return ONLY the JSON array, no other text.
"""


def build_user_prompt(
    pantry_items: List[str],
    diets: List[str],
    allergies: List[str],
    disliked: List[str],
    preferred_cuisines: List[str],
    cuisine_filter: Optional[str],
    servings: int,
    rag_context: str,
) -> str:
    parts = []

    parts.append(f"**My pantry ingredients:** {', '.join(pantry_items) if pantry_items else 'nothing yet'}")

    if diets:
        parts.append(f"**My dietary restrictions:** {', '.join(diets)}")
    if allergies:
        parts.append(f"**My allergies (MUST AVOID):** {', '.join(allergies)}")
    if disliked:
        parts.append(f"**Foods I dislike:** {', '.join(disliked)}")
    if preferred_cuisines:
        parts.append(f"**Preferred cuisines:** {', '.join(preferred_cuisines)}")
    if cuisine_filter:
        parts.append(f"**Cuisine for this request:** {cuisine_filter}")

    parts.append(f"**Servings:** {servings}")

    if rag_context:
        parts.append(f"\n**Reference recipes from knowledge base:**\n{rag_context}")

    parts.append("\nPlease suggest 2-4 recipes I can make. Return ONLY a JSON array.")
    return "\n".join(parts)


def suggest_recipes(
    pantry_items: List[str],
    diets: List[str],
    allergies: List[str],
    disliked: List[str],
    preferred_cuisines: List[str],
    cuisine_filter: Optional[str] = None,
    servings: int = 2,
) -> List[SuggestedRecipe]:
    """Generate recipe suggestions using RAG + LLM."""

    # 1. Build query from pantry for RAG search
    query = " ".join(pantry_items[:20]) if pantry_items else "simple easy recipe"
    if cuisine_filter:
        query += f" {cuisine_filter}"

    # 2. Retrieve relevant recipes from knowledge base
    rag_results = []
    try:
        rag_results = rag_search(query, k=5, cuisine=cuisine_filter)
    except Exception:
        # RAG may be empty or unavailable — that's fine, LLM can still suggest
        pass

    # 3. Build RAG context string
    rag_context = ""
    if rag_results:
        snippets = []
        for r in rag_results:
            meta = r.get("metadata", {})
            title = meta.get("title", "Untitled")
            cuisine = meta.get("cuisine", "")
            doc = r.get("document", "")[:500]
            snippets.append(f"- **{title}** ({cuisine}): {doc}")
        rag_context = "\n".join(snippets)

    # 4. Build messages for LLM
    user_prompt = build_user_prompt(
        pantry_items=pantry_items,
        diets=diets,
        allergies=allergies,
        disliked=disliked,
        preferred_cuisines=preferred_cuisines,
        cuisine_filter=cuisine_filter,
        servings=servings,
        rag_context=rag_context,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    # 5. Call LLM
    raw = chat_text_prompt(messages, temperature=0.5, max_tokens=2000)

    # 6. Parse response into structured recipes
    recipes = _parse_recipes(raw)
    return recipes


def _parse_recipes(raw: str) -> List[SuggestedRecipe]:
    """Parse the LLM's JSON response into SuggestedRecipe objects."""
    try:
        # Find JSON array in response
        start = raw.index("[")
        end = raw.rindex("]") + 1
        data = json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        # Fallback: try to parse the whole response
        try:
            data = json.loads(raw.strip())
        except json.JSONDecodeError:
            return []

    if not isinstance(data, list):
        return []

    recipes = []
    for item in data:
        if not isinstance(item, dict):
            continue
        try:
            missing = []
            for m in item.get("missing", []):
                if isinstance(m, dict):
                    missing.append(
                        MissingItem(
                            name=m.get("name", "unknown"),
                            suggested_quantity=m.get("suggested_quantity"),
                        )
                    )
                elif isinstance(m, str):
                    missing.append(MissingItem(name=m))

            recipe = SuggestedRecipe(
                title=item.get("title", "Untitled"),
                cuisine=item.get("cuisine"),
                ingredients=item.get("ingredients", []),
                missing=missing,
                steps=item.get("steps", []),
                citations=item.get("citations", []),
                score=float(item.get("score", 0.5)),
            )
            recipes.append(recipe)
        except Exception:
            continue

    # Sort by score descending
    recipes.sort(key=lambda r: r.score, reverse=True)
    return recipes
