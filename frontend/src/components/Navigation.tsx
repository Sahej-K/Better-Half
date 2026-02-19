import { NavLink } from "react-router-dom";

const links = [
  { to: "/pantry", label: "🧊 Pantry" },
  { to: "/suggest", label: "🍳 Get Recipes" },
  { to: "/preferences", label: "⚙️ Preferences" },
];

export default function Navigation() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 flex items-center justify-between h-14">
        <span className="text-xl font-bold bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent">
          ChefGenie
        </span>
        <div className="flex gap-1">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-orange-100 text-orange-700"
                    : "text-gray-600 hover:bg-gray-100"
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}
