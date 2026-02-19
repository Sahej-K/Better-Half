import json
from typing import List
from app.services.llm import chat_vision_prompt

VISION_SYSTEM = (
    "You are a kitchen inventory assistant. From the image(s), list the "
    "ingredient items you clearly see. Return ONLY a JSON array of distinct "
    "ingredient names in lowercase (no quantities, no brand names). "
    "Example: [\"eggs\", \"milk\", \"tomato\"]"
)


def extract_ingredients_from_image_url(image_url: str) -> List[str]:
    messages = [
        {"role": "system", "content": VISION_SYSTEM},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Identify the ingredients in this image."},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        },
    ]
    raw = chat_vision_prompt(messages)
    # Try to extract JSON array from the response
    try:
        # Find JSON array in response
        start = raw.index("[")
        end = raw.rindex("]") + 1
        arr = json.loads(raw[start:end])
        if isinstance(arr, list):
            return [str(x).lower().strip() for x in arr if x]
    except (ValueError, json.JSONDecodeError):
        pass
    return []
