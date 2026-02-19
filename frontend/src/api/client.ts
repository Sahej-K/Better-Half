import axios from "axios";
import type { PantryItem, Preferences, SuggestResponse } from "../types/api";

// In dev, Vite proxy forwards /pantry etc to localhost:8000
// In production build, the backend serves the frontend
const api = axios.create({ baseURL: "/" });

// ── Pantry ──────────────────────────────────────────────
export async function getPantry(): Promise<PantryItem[]> {
  const { data } = await api.get("/pantry");
  return data;
}

export async function addPantryItem(
  name: string,
  quantity?: string
): Promise<PantryItem> {
  const { data } = await api.post("/pantry", { name, quantity });
  return data;
}

export async function deletePantryItem(id: number): Promise<void> {
  await api.delete(`/pantry/${id}`);
}

export async function clearPantry(): Promise<void> {
  await api.delete("/pantry");
}

// ── Preferences ─────────────────────────────────────────
export async function getPreferences(): Promise<Preferences> {
  const { data } = await api.get("/preferences");
  return data;
}

export async function updatePreferences(
  prefs: Partial<Preferences>
): Promise<Preferences> {
  const { data } = await api.put("/preferences", prefs);
  return data;
}

// ── Recipes ─────────────────────────────────────────────
export async function suggestRecipes(
  cuisine?: string
): Promise<SuggestResponse> {
  const { data } = await api.post("/recipes/suggest", {
    cuisine: cuisine || null,
    servings: 2,
    allow_missing: true,
  });
  return data;
}

// ── Vision ──────────────────────────────────────────────
export async function analyzeImage(
  imageUrl: string
): Promise<{ detected_items: string[]; added_count: number }> {
  const { data } = await api.post("/vision/pantry", {
    image_url: imageUrl,
    add_to_pantry: true,
  });
  return data;
}
