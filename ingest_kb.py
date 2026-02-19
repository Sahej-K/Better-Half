"""
Ingest recipe markdown files into the ChromaDB vector store.
Run once after adding/changing recipes in app/kb/recipes/.

Usage:
    python ingest_kb.py
"""
import os, yaml, glob
from app.services.rag import upsert_recipe_docs


def load_recipe_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        raise ValueError(f"No YAML front matter in {path}")

    parts = content.split("---", 2)
    meta = yaml.safe_load(parts[1])
    body = parts[2].strip() if len(parts) > 2 else ""

    # Build a rich text blob for embedding
    ingredients = meta.get("ingredients", [])
    full_text = f"{meta.get('title','')}\nCuisine: {meta.get('cuisine','')}\n"
    full_text += f"Ingredients: {', '.join(ingredients)}\n{body}"

    return {
        "id": meta.get("id") or os.path.splitext(os.path.basename(path))[0],
        "title": meta.get("title", ""),
        "cuisine": meta.get("cuisine", ""),
        "tags": meta.get("tags", []),
        "ingredients": ingredients,
        "content": full_text,
        "path": path,
    }


def main():
    base = os.path.join(os.path.dirname(__file__), "app", "kb", "recipes")
    paths = sorted(glob.glob(os.path.join(base, "*.md")))
    if not paths:
        print(f"No recipe .md files found in {base}")
        return
    docs = [load_recipe_file(p) for p in paths]
    upsert_recipe_docs(docs)
    print(f"✅ Ingested {len(docs)} recipes into ChromaDB")
    for d in docs:
        print(f"   - {d['title']} ({d['cuisine']})")


if __name__ == "__main__":
    main()
