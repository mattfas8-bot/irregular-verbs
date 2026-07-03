import { VERBS } from "./data/verbs";
import { LESSONS } from "./data/lessons";

const STORAGE_KEY = "tajik-verbs-progress";

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completedLessons: [], studiedWords: [] };
    return JSON.parse(raw);
  } catch {
    return { completedLessons: [], studiedWords: [] };
  }
}

function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

export const api = {
  progress() {
    const state = loadState();
    const lessonsTotal = LESSONS.length;
    const lessonsCompleted = state.completedLessons.length;
    const pct = lessonsTotal ? lessonsCompleted / lessonsTotal : 0;
    return Promise.resolve({
      level: pct >= 0.7 ? "A2" : "A1",
      lessons_completed: lessonsCompleted,
      lessons_total: lessonsTotal,
      words_total: VERBS.length,
      irregular_verbs: VERBS.length,
    });
  },

  lessons() {
    const state = loadState();
    return Promise.resolve(
      LESSONS.map((l) => ({ ...l, completed: state.completedLessons.includes(l.id) }))
    );
  },

  completeLesson(id) {
    const state = loadState();
    if (!state.completedLessons.includes(id)) {
      state.completedLessons.push(id);
      saveState(state);
    }
    return Promise.resolve();
  },

  vocabulary() {
    return Promise.resolve(VERBS);
  },
};
