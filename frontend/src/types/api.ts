export interface PantryItem {
  id: number;
  name: string;
  quantity?: string | null;
  notes?: string | null;
}

export interface Preferences {
  diets: string[];
  allergies: string[];
  disliked: string[];
  preferred_cuisines: string[];
}

export interface MissingItem {
  name: string;
  suggested_quantity?: string | null;
}

export interface Recipe {
  title: string;
  cuisine?: string | null;
  ingredients: string[];
  missing: MissingItem[];
  steps: string[];
  citations: string[];
  score: number;
}

export interface SuggestResponse {
  recipes: Recipe[];
}
