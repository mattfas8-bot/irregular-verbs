import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Lessons from "./pages/Lessons";
import Vocabulary from "./pages/Vocabulary";

export default function App() {
  const [page, setPage] = useState("dashboard");

  if (page === "lessons") return <Lessons onNavigate={setPage} />;
  if (page === "vocabulary") return <Vocabulary onNavigate={setPage} />;
  return <Dashboard onNavigate={setPage} />;
}
