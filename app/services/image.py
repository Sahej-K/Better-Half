from typing import List
from app.services.llm import chat_vision_prompt

VISION_SYSTEM = (
    "You are a kitchen inventory assistant. From the image(s), list the ingredient items you clearly see. "
    "Return a short JSON array of distinct ingredient names in lowercase (no quantities, no brand names)."
)

def extract_ingredients_from_image_url(image_url: str) -> List[str]:
    messages = [
        {"role": "system", "content": [{"type": "text", "text": VISION_SYSTEM}]},
        {"role": "user", "content": [
            {"type": "text", "text": "Identify ingredients."},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]}
    ]
    raw = chat_vision_prompt(messages)
    import json
    try:
        arr = json.loads(raw.strip().split("\n")[-1])
        if isinstance(arr, list):
            return [str(x).lower().strip() for x in arr]
    except Exception:
        pass
    return []
