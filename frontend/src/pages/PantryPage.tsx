import { useState, useEffect } from "react";
import {
  getPantry,
  addPantryItem,
  deletePantryItem,
  clearPantry,
  analyzeImage,
} from "../api/client";
import type { PantryItem } from "../types/api";

export default function PantryPage() {
  const [items, setItems] = useState<PantryItem[]>([]);
  const [name, setName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [loading, setLoading] = useState(true);

  // Image analysis
  const [imageUrl, setImageUrl] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<string[] | null>(null);

  const refresh = async () => {
    setLoading(true);
    try {
      setItems(await getPantry());
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  useEffect(() => {
    refresh();
  }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    await addPantryItem(name.trim(), quantity.trim() || undefined);
    setName("");
    setQuantity("");
    refresh();
  };

  const handleDelete = async (id: number) => {
    await deletePantryItem(id);
    refresh();
  };

  const handleClear = async () => {
    if (!confirm("Remove all pantry items?")) return;
    await clearPantry();
    refresh();
  };

  const handleAnalyze = async () => {
    if (!imageUrl.trim()) return;
    setAnalyzing(true);
    setAnalysisResult(null);
    try {
      const res = await analyzeImage(imageUrl.trim());
      setAnalysisResult(res.detected_items);
      refresh(); // they got added to pantry
    } catch (e) {
      alert("Image analysis failed. Make sure your OpenAI key supports vision.");
    }
    setAnalyzing(false);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">🧊 My Pantry</h1>
        <p className="text-gray-500 mt-1">
          Add ingredients you have at home. ChefGenie will suggest recipes using
          them.
        </p>
      </div>

      {/* Add item form */}
      <form onSubmit={handleAdd} className="flex gap-3">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Ingredient name (e.g. eggs)"
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none"
        />
        <input
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          placeholder="Qty (optional)"
          className="w-32 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none"
        />
        <button
          type="submit"
          className="px-5 py-2 bg-orange-500 text-white rounded-lg font-medium hover:bg-orange-600 transition-colors"
        >
          + Add
        </button>
      </form>

      {/* Image analysis section */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">
          📸 Add from Image
        </h2>
        <div className="flex gap-3">
          <input
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            placeholder="Paste an image URL of your fridge or groceries"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none text-sm"
          />
          <button
            onClick={handleAnalyze}
            disabled={analyzing || !imageUrl.trim()}
            className="px-4 py-2 bg-purple-500 text-white rounded-lg text-sm font-medium hover:bg-purple-600 transition-colors disabled:opacity-50"
          >
            {analyzing ? "Analyzing…" : "Analyze"}
          </button>
        </div>
        {analysisResult && (
          <div className="mt-3 p-3 bg-green-50 rounded-lg">
            <p className="text-sm text-green-700 font-medium">
              ✅ Detected & added: {analysisResult.join(", ")}
            </p>
          </div>
        )}
      </div>

      {/* Pantry items grid */}
      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : items.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          <p className="text-4xl mb-2">🧺</p>
          <p>Your pantry is empty. Add some ingredients above!</p>
        </div>
      ) : (
        <>
          <div className="flex justify-between items-center">
            <p className="text-sm text-gray-500">
              {items.length} ingredient{items.length !== 1 && "s"}
            </p>
            <button
              onClick={handleClear}
              className="text-xs text-red-500 hover:text-red-700"
            >
              Clear all
            </button>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {items.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-lg border border-gray-200 p-3 flex items-center justify-between group"
              >
                <div>
                  <p className="font-medium text-sm text-gray-800 capitalize">
                    {item.name}
                  </p>
                  {item.quantity && (
                    <p className="text-xs text-gray-400">{item.quantity}</p>
                  )}
                </div>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="text-gray-300 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
