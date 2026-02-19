import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navigation from "./components/Navigation";
import PantryPage from "./pages/PantryPage";
import SuggestPage from "./pages/SuggestPage";
import PreferencesPage from "./pages/PreferencesPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <main className="max-w-5xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Navigate to="/pantry" replace />} />
            <Route path="/pantry" element={<PantryPage />} />
            <Route path="/suggest" element={<SuggestPage />} />
            <Route path="/preferences" element={<PreferencesPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
