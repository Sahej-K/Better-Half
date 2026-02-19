from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text
from app.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    diets: Mapped[str | None] = mapped_column(String, nullable=True)
    allergies: Mapped[str | None] = mapped_column(String, nullable=True)
    disliked: Mapped[str | None] = mapped_column(String, nullable=True)
    preferred_cuisines: Mapped[str | None] = mapped_column(String, nullable=True)


class PantryItem(Base):
    __tablename__ = "pantry_items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)
    quantity: Mapped[str | None] = mapped_column(String, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class KBRecipeIndex(Base):
    __tablename__ = "kb_recipes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kb_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    title: Mapped[str] = mapped_column(String)
    cuisine: Mapped[str | None] = mapped_column(String)
    tags: Mapped[str | None] = mapped_column(String)
    raw_path: Mapped[str] = mapped_column(String)
    metadata_json: Mapped[str | None] = mapped_column(Text)
