import { useEffect, useState } from "react";
import { api } from "../api";
import ErrorState from "../components/ErrorState";

function LessonQuiz({ lesson, onDone }) {
  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState(null);
  const [correctCount, setCorrectCount] = useState(0);

  const q = lesson.questions[idx];

  function choose(opt) {
    if (selected) return;
    setSelected(opt);
    if (opt === q.answer) setCorrectCount((c) => c + 1);
    setTimeout(() => {
      if (idx + 1 < lesson.questions.length) {
        setIdx((i) => i + 1);
        setSelected(null);
      } else {
        onDone(correctCount + (opt === q.answer ? 1 : 0));
      }
    }, 700);
  }

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <p className="mb-3 text-xs text-gray-400">
        Савол {idx + 1} / {lesson.questions.length}
      </p>
      <p className="mb-4 text-lg font-semibold text-gray-800">{q.q}</p>
      <div className="space-y-2">
        {q.options.map((opt) => {
          const isAnswer = opt === q.answer;
          const isSelected = opt === selected;
          let style = "border-gray-200 bg-white hover:border-indigo-300";
          if (selected) {
            if (isAnswer) style = "border-emerald-500 bg-emerald-50 text-emerald-700";
            else if (isSelected) style = "border-rose-500 bg-rose-50 text-rose-700";
          }
          return (
            <button
              key={opt}
              disabled={!!selected}
              onClick={() => choose(opt)}
              className={`w-full rounded-xl border px-4 py-3 text-left text-sm font-medium transition ${style}`}
            >
              {opt}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default function Lessons({ onNavigate }) {
  const [lessons, setLessons] = useState(null);
  const [error, setError] = useState(false);
  const [activeId, setActiveId] = useState(null);
  const [result, setResult] = useState(null);

  function reload() {
    api
      .lessons()
      .then(setLessons)
      .catch((e) => {
        console.error("Хатои боргирии дарсҳо:", e);
        setError(true);
      });
  }

  useEffect(reload, []);

  if (error)
    return <ErrorState message="Дарсҳо дастрас нестанд. Лутфан баъдтар кӯшиш кунед." />;
  if (!lessons) return <p className="p-6 text-center text-gray-400">Бор шуда истодааст…</p>;

  const active = lessons.find((l) => l.id === activeId);

  function finishLesson(correctCount) {
    api.completeLesson(active.id).then(() => {
      setResult({ correctCount, total: active.questions.length });
      reload();
    });
  }

  function backToList() {
    setActiveId(null);
    setResult(null);
  }

  return (
    <div className="mx-auto max-w-2xl p-4">
      <div className="mb-4 flex items-center gap-3">
        <button
          onClick={() => (active ? backToList() : onNavigate("dashboard"))}
          className="text-sm font-medium text-indigo-600 hover:underline"
        >
          ← Бозгашт
        </button>
        <h1 className="text-xl font-extrabold text-gray-800">Дарсҳои грамматика</h1>
      </div>

      {!active && (
        <div className="space-y-3">
          {lessons.map((l) => (
            <button
              key={l.id}
              onClick={() => {
                setActiveId(l.id);
                setResult(null);
              }}
              className="flex w-full items-center justify-between rounded-2xl border border-gray-200 bg-white p-4 text-left shadow-sm transition hover:shadow-md"
            >
              <div>
                <div className="font-bold text-gray-800">{l.title}</div>
                <div className="text-sm text-gray-500">{l.subtitle}</div>
              </div>
              {l.completed && (
                <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">
                  Тамом ✓
                </span>
              )}
            </button>
          ))}
        </div>
      )}

      {active && !result && (
        <div className="space-y-4">
          <div className="rounded-2xl bg-indigo-50 p-4 text-sm text-indigo-900">
            {active.explanation}
          </div>
          <LessonQuiz lesson={active} onDone={finishLesson} />
        </div>
      )}

      {active && result && (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 text-center shadow-sm">
          <div className="text-3xl">🎉</div>
          <h2 className="mt-2 text-lg font-bold text-gray-800">Дарс тамом шуд!</h2>
          <p className="mt-1 text-sm text-gray-500">
            Дуруст: {result.correctCount} / {result.total}
          </p>
          <button
            onClick={backToList}
            className="mt-4 rounded-xl bg-indigo-600 px-5 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
          >
            Ба рӯйхати дарсҳо
          </button>
        </div>
      )}
    </div>
  );
}
