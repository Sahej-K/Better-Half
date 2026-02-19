import type { Recipe } from "../types/api";

export default function RecipeCard({ recipe }: { recipe: Recipe }) {
  const pct = Math.round(recipe.score * 100);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="p-5 border-b border-gray-100">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {recipe.title}
            </h3>
            {recipe.cuisine && (
              <span className="inline-block mt-1 text-xs font-medium px-2 py-0.5 rounded-full bg-orange-100 text-orange-700">
                {recipe.cuisine}
              </span>
            )}
          </div>
          <div className="flex flex-col items-center">
            <div className="text-2xl font-bold text-orange-600">{pct}%</div>
            <div className="text-xs text-gray-400">match</div>
          </div>
        </div>
        {/* Score bar */}
        <div className="mt-3 w-full bg-gray-100 rounded-full h-2">
          <div
            className="h-2 rounded-full bg-gradient-to-r from-orange-400 to-red-500 transition-all"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      {/* Ingredients */}
      <div className="p-5 border-b border-gray-100">
        <h4 className="text-sm font-semibold text-gray-700 mb-2">
          Ingredients
        </h4>
        <div className="flex flex-wrap gap-1.5">
          {recipe.ingredients.map((ing, i) => {
            const isMissing = recipe.missing.some(
              (m) => m.name.toLowerCase() === ing.toLowerCase()
            );
            return (
              <span
                key={i}
                className={`text-xs px-2 py-1 rounded-full ${
                  isMissing
                    ? "bg-red-50 text-red-600 border border-red-200"
                    : "bg-green-50 text-green-700 border border-green-200"
                }`}
              >
                {ing}
                {isMissing && " ✗"}
              </span>
            );
          })}
        </div>
        {recipe.missing.length > 0 && (
          <p className="mt-2 text-xs text-gray-400">
            🔴 Red = you need to buy &nbsp; 🟢 Green = you have it
          </p>
        )}
      </div>

      {/* Steps */}
      <div className="p-5">
        <h4 className="text-sm font-semibold text-gray-700 mb-2">Steps</h4>
        <ol className="space-y-2">
          {recipe.steps.map((step, i) => (
            <li key={i} className="flex gap-3 text-sm text-gray-600">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-orange-100 text-orange-700 flex items-center justify-center text-xs font-bold">
                {i + 1}
              </span>
              <span>{step.replace(/^(Step )?\d+[:.]\s*/i, "")}</span>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
