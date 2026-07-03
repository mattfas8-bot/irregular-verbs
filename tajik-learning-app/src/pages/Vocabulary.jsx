import { useEffect, useState } from "react";
import { api } from "../api";
import ErrorState from "../components/ErrorState";

export default function Vocabulary({ onNavigate }) {
  const [words, setWords] = useState(null);
  const [error, setError] = useState(false);
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);

  useEffect(() => {
    api
      .vocabulary()
      .then(setWords)
      .catch((e) => {
        console.error("Хатои боргирии луғат:", e);
        setError(true);
      });
  }, []);

  if (error)
    return <ErrorState message="Луғат дастрас нест. Лутфан баъдтар кӯшиш кунед." />;
  if (!words) return <p className="p-6 text-center text-gray-400">Бор шуда истодааст…</p>;

  const word = words[idx];

  function next() {
    setFlipped(false);
    setIdx((i) => (i + 1) % words.length);
  }

  function prev() {
    setFlipped(false);
    setIdx((i) => (i - 1 + words.length) % words.length);
  }

  return (
    <div className="mx-auto max-w-md p-4">
      <div className="mb-4 flex items-center gap-3">
        <button
          onClick={() => onNavigate("dashboard")}
          className="text-sm font-medium text-indigo-600 hover:underline"
        >
          ← Бозгашт
        </button>
        <h1 className="text-xl font-extrabold text-gray-800">Кортҳои луғат</h1>
      </div>

      <p className="mb-2 text-center text-xs text-gray-400">
        {idx + 1} / {words.length}
      </p>

      <button
        onClick={() => setFlipped((f) => !f)}
        className="flex min-h-[220px] w-full flex-col items-center justify-center gap-2 rounded-3xl border border-gray-200 bg-white p-8 text-center shadow-sm transition hover:shadow-md"
      >
        <div className="text-3xl font-extrabold text-gray-800">{word.base}</div>
        <div className="text-sm text-gray-400">{word.ipa}</div>
        {flipped && (
          <>
            <div className="mt-3 text-lg font-semibold text-rose-600">
              {word.base} – {word.past} – {word.participle}
            </div>
            <div className="mt-1 text-lg font-medium text-emerald-600">{word.tj}</div>
          </>
        )}
        {!flipped && (
          <div className="mt-3 text-xs italic text-gray-400">
            барои дидани тарҷума пахш кунед
          </div>
        )}
      </button>

      <div className="mt-4 flex gap-3">
        <button
          onClick={prev}
          className="flex-1 rounded-xl border border-gray-200 bg-white py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50"
        >
          ← Пеш
        </button>
        <button
          onClick={next}
          className="flex-1 rounded-xl bg-indigo-600 py-3 text-sm font-semibold text-white hover:bg-indigo-700"
        >
          Оянда →
        </button>
      </div>
    </div>
  );
}
