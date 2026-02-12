import os, yaml, glob
from app.services.rag import upsert_recipe_docs

def load_recipe_file(path: str):
    # simple YAML front matter parser
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        meta = yaml.safe_load(parts[1])
        rest = parts[2].strip()
        return {
            "id": meta.get("id") or os.path.basename(path),
            "title": meta.get("title"),
            "cuisine": meta.get("cuisine"),
            "tags": meta.get("tags", []),
            "ingredients": meta.get("ingredients", []),
            "content": (meta.get("content") or "") + "\n" + rest,
            "path": path,
        }
    else:
        raise ValueError(f"No YAML front matter in {path}")

def main():
    base = os.path.join(os.path.dirname(__file__), "app", "kb", "recipes")
    paths = glob.glob(os.path.join(base, "*.md"))
    docs = [load_recipe_file(p) for p in paths]
    upsert_recipe_docs(docs)
    print(f"Ingested {len(docs)} recipes into ChromaDB")

if __name__ == "__main__":
    main()
