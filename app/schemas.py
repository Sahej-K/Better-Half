<<<<<<< HEAD
from pydantic import BaseModel
from typing import List, Optional


=======
from pydantic import BaseModel, Field
from typing import List, Optional

>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class PreferenceUpdate(BaseModel):
    diets: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    disliked: Optional[List[str]] = None
    preferred_cuisines: Optional[List[str]] = None

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class PreferenceOut(BaseModel):
    diets: List[str] = []
    allergies: List[str] = []
    disliked: List[str] = []
    preferred_cuisines: List[str] = []

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class PantryItemCreate(BaseModel):
    name: str
    quantity: Optional[str] = None
    notes: Optional[str] = None

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class PantryItemOut(BaseModel):
    id: int
    name: str
    quantity: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class VisionIn(BaseModel):
    image_url: Optional[str] = None
    add_to_pantry: bool = True

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class VisionOut(BaseModel):
    detected_items: List[str]
    added_count: int

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class SuggestRequest(BaseModel):
    cuisine: Optional[str] = None
    servings: Optional[int] = 2
    allow_missing: bool = True
    pantry_override: Optional[List[str]] = None

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class MissingItem(BaseModel):
    name: str
    suggested_quantity: Optional[str] = None

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class SuggestedRecipe(BaseModel):
    title: str
    cuisine: Optional[str] = None
    ingredients: List[str]
    missing: List[MissingItem]
    steps: List[str]
    citations: List[str] = []
    score: float

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
class SuggestResponse(BaseModel):
    recipes: List[SuggestedRecipe]
