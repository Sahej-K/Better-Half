from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, JSON, Text
from app.database import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # In a real app, link to user_id (auth). For demo, we assume one profile.
    diets: Mapped[str | None] = mapped_column(String, nullable=True)        # e.g., "vegetarian,kosher"
    allergies: Mapped[str | None] = mapped_column(String, nullable=True)    # e.g., "peanuts,shellfish"
    disliked: Mapped[str | None] = mapped_column(String, nullable=True)     # e.g., "olives,cilantro"
    preferred_cuisines: Mapped[str | None] = mapped_column(String, nullable=True)

class PantryItem(Base):
    __tablename__ = "pantry_items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)
    quantity: Mapped[str | None] = mapped_column(String, nullable=True)     # free text "2 cups"
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

# Optional: store references to KB recipes synced into the app DB
class KBRecipeIndex(Base):
    __tablename__ = "kb_recipes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kb_id: Mapped[str] = mapped_column(String, unique=True, index=True)     # path or unique doc id
    title: Mapped[str] = mapped_column(String)
    cuisine: Mapped[str | None] = mapped_column(String)
    tags: Mapped[str | None] = mapped_column(String)
    raw_path: Mapped[str] = mapped_column(String)                            # file path in repo
    metadata_json: Mapped[str | None] = mapped_column(Text)                  # JSON string if needed
``