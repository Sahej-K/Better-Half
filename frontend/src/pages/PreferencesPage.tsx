import { useState, useEffect } from "react";
import { getPreferences, updatePreferences } from "../api/client";
import type { Preferences } from "../types/api";

const DIET_OPTIONS = [
  "vegetarian",
  "vegan",
  "pescatarian",
  "keto",
  "paleo",
  "gluten-free",
  "halal",
  "kosher",
];

const ALLERGY_OPTIONS = [
  "peanuts",
  "tree nuts",
  "dairy",
  "eggs",
  "soy",
  "wheat",
  "shellfish",
  "fish",
];

const CUISINE_OPTIONS = [
  "italian",
  "indian",
  "asian",
  "mexican",
  "french",
  "middle eastern",
  "american",
  "mediterranean",
];

export default function PreferencesPage() {
  const [prefs, setPrefs] = useState<Preferences>({
    diets: [],
    allergies: [],
    disliked: [],
    preferred_cuisines: [],
  });
  const [dislikedInput, setDislikedInput] = useState("");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    getPreferences().then(setPrefs).catch(console.error);
  }, []);

  const toggle = (
    field: "diets" | "allergies" | "preferred_cuisines",
    value: string
  ) => {
    setPrefs((p) => ({
      ...p,
      [field]: p[field].includes(value)
        ? p[field].filter((v) => v !== value)
        : [...p[field], value],
    }));
  };

  const addDisliked = () => {
    const val = dislikedInput.trim().toLowerCase();
    if (!val || prefs.disliked.includes(val)) return;
    setPrefs((p) => ({ ...p, disliked: [...p.disliked, val] }));
    setDislikedInput("");
  };

  const removeDisliked = (val: string) => {
    setPrefs((p) => ({
      ...p,
      disliked: p.disliked.filter((d) => d !== val),
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    setSaved(false);
    try {
      const updated = await updatePreferences(prefs);
      setPrefs(updated);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (e) {
      alert("Failed to save preferences");
    }
    setSaving(false);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">⚙️ Preferences</h1>
        <p className="text-gray-500 mt-1">
          Tell ChefGenie about your diet so it never suggests something you
          can't eat.
        </p>
      </div>

      {/* Diets */}
      <Section title="Dietary Restrictions">
        <div className="flex flex-wrap gap-2">
          {DIET_OPTIONS.map((d) => (
            <ToggleChip
              key={d}
              label={d}
              active={prefs.diets.includes(d)}
              onClick={() => toggle("diets", d)}
            />
          ))}
        </div>
      </Section>

      {/* Allergies */}
      <Section title="Allergies (will NEVER appear in recipes)">
        <div className="flex flex-wrap gap-2">
          {ALLERGY_OPTIONS.map((a) => (
            <ToggleChip
              key={a}
              label={a}
              active={prefs.allergies.includes(a)}
              onClick={() => toggle("allergies", a)}
              activeColor="bg-red-100 text-red-700 border-red-300"
            />
          ))}
        </div>
      </Section>

      {/* Preferred cuisines */}
      <Section title="Preferred Cuisines">
        <div className="flex flex-wrap gap-2">
          {CUISINE_OPTIONS.map((c) => (
            <ToggleChip
              key={c}
              label={c}
              active={prefs.preferred_cuisines.includes(c)}
              onClick={() => toggle("preferred_cuisines", c)}
              activeColor="bg-blue-100 text-blue-700 border-blue-300"
            />
          ))}
        </div>
      </Section>

      {/* Disliked foods */}
      <Section title="Disliked Foods">
        <div className="flex gap-2 mb-3">
          <input
            value={dislikedInput}
            onChange={(e) => setDislikedInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addDisliked())}
            placeholder="e.g. cilantro"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-orange-300 focus:border-orange-400 outline-none"
          />
          <button
            onClick={addDisliked}
            className="px-4 py-2 bg-gray-200 rounded-lg text-sm font-medium hover:bg-gray-300"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {prefs.disliked.map((d) => (
            <span
              key={d}
              className="inline-flex items-center gap-1 text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600 border border-gray-200"
            >
              {d}
              <button
                onClick={() => removeDisliked(d)}
                className="text-gray-400 hover:text-red-500"
              >
                ✕
              </button>
            </span>
          ))}
          {prefs.disliked.length === 0 && (
            <p className="text-xs text-gray-400">None added yet</p>
          )}
        </div>
      </Section>

      {/* Save */}
      <button
        onClick={handleSave}
        disabled={saving}
        className="px-6 py-2.5 bg-orange-500 text-white rounded-lg font-medium hover:bg-orange-600 transition-colors disabled:opacity-50"
      >
        {saving ? "Saving…" : saved ? "✅ Saved!" : "Save Preferences"}
      </button>
    </div>
  );
}

// ── Helper components ───────────────────────────────────

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h2 className="text-sm font-semibold text-gray-700 mb-3">{title}</h2>
      {children}
    </div>
  );
}

function ToggleChip({
  label,
  active,
  onClick,
  activeColor = "bg-orange-100 text-orange-700 border-orange-300",
}: {
  label: string;
  active: boolean;
  onClick: () => void;
  activeColor?: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`text-xs px-3 py-1.5 rounded-full border font-medium capitalize transition-colors ${
        active ? activeColor : "bg-white text-gray-500 border-gray-200 hover:bg-gray-50"
      }`}
    >
      {label}
    </button>
  );
}
