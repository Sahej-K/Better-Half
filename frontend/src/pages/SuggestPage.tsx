import { useState } from "react";
import { suggestRecipes } from "../api/client";
import RecipeCard from "../components/RecipeCard";
import type { Recipe } from "../types/api";

const CUISINES = [
  "Any",
  "Italian",
  "Indian",
  "Asian",
  "Mexican",
  "French",
  "Middle Eastern",
  "American",
];

export default function SuggestPage() {
  const [cuisine, setCuisine] = useState("Any");
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSuggest = async () => {
    setLoading(true);
    setError("");
    setRecipes([]);
    try {
      const res = await suggestRecipes(
        cuisine === "Any" ? undefined : cuisine.toLowerCase()
      );
      setRecipes(res.recipes);
      if (res.recipes.length === 0) {
        setError("No recipes found. Try adding more ingredients to your pantry!");
      }
    } catch (e: any) {
      setError(
        e?.response?.data?.detail ||
          "Failed to get suggestions. Check that the backend is running and your OpenAI key is set."
      );
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">🍳 Get Recipes</h1>
        <p className="text-gray-500 mt-1">
          ChefGenie will suggest recipes based on what's in your pantry and your
          preferences.
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap gap-3 items-end">
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">
            Cuisine
          </label>
          <select
            value={cuisine}
            onChange={(e) => setCuisine(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none"
          >
            {CUISINES.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </div>
        <button
          onClick={handleSuggest}
          disabled={loading}
          className="px-6 py-2 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-lg font-medium hover:from-orange-600 hover:to-red-600 transition-all disabled:opacity-50"
        >
          {loading ? "Thinking…" : "✨ Suggest Recipes"}
        </button>
      </div>

      {/* Loading state */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500" />
          <p className="mt-3 text-gray-500">
            ChefGenie is crafting recipes for you…
          </p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Recipe results */}
      {recipes.length > 0 && (
        <div className="grid gap-6 md:grid-cols-2">
          {recipes.map((r, i) => (
            <RecipeCard key={i} recipe={r} />
          ))}
        </div>
      )}
    </div>
  );
}
