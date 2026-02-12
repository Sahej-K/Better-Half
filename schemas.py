from pydantic import BaseModel, Field
from typing import List, Optional

class PreferenceUpdate(BaseModel):
    diets: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    disliked: Optional[List[str]] = None
    preferred_cuisines: Optional[List[str]] = None

class PreferenceOut(BaseModel):
    diets: List[str] = []
    allergies: List[str] = []
    disliked: List[str] = []
    preferred_cuisines: List[str] = []

class PantryItemCreate(BaseModel):
    name: str
    quantity: Optional[str] = None
    notes: Optional[str] = None

class PantryItemOut(BaseModel):
    id: int
    name: str
    quantity: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class VisionIn(BaseModel):
    image_url: Optional[str] = None
    add_to_pantry: bool = True

class VisionOut(BaseModel):
    detected_items: List[str]
    added_count: int

class SuggestRequest(BaseModel):
    cuisine: Optional[str] = None
    servings: Optional[int] = 2
    allow_missing: bool = True
    # override pantry (optional)
    pantry_override: Optional[List[str]] = None

class MissingItem(BaseModel):
    name: str
    suggested_quantity: Optional[str] = None

class SuggestedRecipe(BaseModel):
    title: str
    cuisine: Optional[str] = None
    ingredients: List[str]
    missing: List[MissingItem]
    steps: List[str]
    citations: List[str] = []  # KB doc ids
    score: float

class SuggestResponse(BaseModel):
    recipes: List[SuggestedRecipe]