import { useEffect, useState } from "react";
import { api } from "../api";
import ErrorState from "../components/ErrorState";

function StatCard({ value, label, gradient }) {
  return (
    <div className={`rounded-2xl bg-gradient-to-br ${gradient} p-4 text-white shadow`}>
      <div className="text-2xl font-extrabold">{value}</div>
      <div className="mt-1 text-xs opacity-80">{label}</div>
    </div>
  );
}

/* Ситораи 5-кунҷа барои парчам */
function Star({ cx, cy, r = 3 }) {
  const ri = r * 0.4;
  const pts = Array.from({ length: 10 }, (_, i) => {
    const angle = (Math.PI / 5) * i - Math.PI / 2;
    const radius = i % 2 === 0 ? r : ri;
    return `${cx + radius * Math.cos(angle)},${cy + radius * Math.sin(angle)}`;
  }).join(" ");
  return <polygon points={pts} />;
}

/* Парчами Тоҷикистон — SVG бо анимасияи CSS (бодхӯрда) */
function TajFlag() {
  // 7 ситора дар камон: маркази (150, 87), шуоъ 26, кунҷҳо аз 30° то 150°
  const starPos = [30, 50, 70, 90, 110, 130, 150].map((deg) => {
    const rad = (deg * Math.PI) / 180;
    return [150 + 26 * Math.cos(rad), 87 - 26 * Math.sin(rad)];
  });

  return (
    <svg
      viewBox="0 0 300 150"
      xmlns="http://www.w3.org/2000/svg"
      width="100%"
      height="100%"
      preserveAspectRatio="xMidYMid slice"
    >
      <defs>
        {/*
          CSS-анимасия дар дохили SVG — кор мекунад дар ҳама браузерҳо.
          Мавҷи бод: skewX + scaleX дар давра, transform-origin ба чап —
          монанди парчам ба мех овезон ба боди мулоим.
        */}
        <style>{`
          @keyframes flagWave {
            0%   { transform: skewX(0deg)    scaleX(1.000) scaleY(1.000); }
            15%  { transform: skewX(1.2deg)  scaleX(1.006) scaleY(0.997); }
            30%  { transform: skewX(2.5deg)  scaleX(1.012) scaleY(0.993); }
            50%  { transform: skewX(3.0deg)  scaleX(1.014) scaleY(0.991); }
            65%  { transform: skewX(2.0deg)  scaleX(1.009) scaleY(0.995); }
            80%  { transform: skewX(0.6deg)  scaleX(1.003) scaleY(0.999); }
            100% { transform: skewX(0deg)    scaleX(1.000) scaleY(1.000); }
          }
          .taj-wave {
            animation: flagWave 4s ease-in-out infinite;
            transform-origin: 0% 50%;
            transform-box: fill-box;
          }
        `}</style>

        {/* Бофтаи матои парчам (статикӣ) */}
        <filter id="cloth-tex" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.025 0.1" numOctaves="3" seed="5" result="noise"/>
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="8" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
      </defs>

      {/* Тамоми парчам — як гурӯҳ, ки мавҷ мекунад */}
      <g className="taj-wave" filter="url(#cloth-tex)">
        {/* Навори сурх */}
        <rect x="-30" y="0" width="360" height="42.86" fill="#D80000" />
        {/* Навори сафед */}
        <rect x="-30" y="42.86" width="360" height="64.28" fill="#FFFFFF" />
        {/* Навори сабз */}
        <rect x="-30" y="107.14" width="360" height="42.86" fill="#007A33" />

        {/* Тоҷ ва ситораҳо — тиллоӣ */}
        <g fill="#FFD700">
          {starPos.map(([cx, cy], i) => (
            <Star key={i} cx={cx} cy={cy} r={3} />
          ))}
          <path d="M131,93 L131,87 L136,87 Q137,80 139,76 Q141,80 142,83 L148,83 Q149,75 150,71 Q151,75 152,83 L158,83 Q159,80 161,76 Q163,80 164,87 L169,87 L169,93 Z" />
          <rect x="131" y="86.5" width="38" height="1.5" />
          <circle cx="139" cy="76" r="2.5" />
          <circle cx="150" cy="71" r="3" />
          <circle cx="161" cy="76" r="2.5" />
        </g>
      </g>
    </svg>
  );
}

export default function Dashboard({ onNavigate }) {
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .progress()
      .then(setProgress)
      .catch((e) => {
        console.error("Хатои боргирии пешрафт:", e);
        setError(true);
      });
  }, []);

  if (error)
    return <ErrorState message="Маълумоти пешрафт дастрас нест. Лутфан баъдтар кӯшиш кунед." />;
  if (!progress) return <p className="p-6 text-center text-gray-400">Бор шуда истодааст…</p>;

  const pct = progress.lessons_total
    ? Math.round((progress.lessons_completed / progress.lessons_total) * 100)
    : 0;

  return (
    <div className="relative mx-auto max-w-3xl p-4">
      {/* Парчами Тоҷикистон — замина бо анимасия, васеъ ба тамоми экран */}
      <div
        className="pointer-events-none absolute inset-0 z-0 overflow-hidden"
        style={{ opacity: 0.55 }}
        aria-hidden
      >
        <TajFlag />
      </div>

      <div className="relative z-10 space-y-5">
        {/* Корти асосӣ */}
        <div className="rounded-3xl bg-gradient-to-br from-indigo-600 to-violet-600 p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-extrabold">Хуш омадед! 👋</h1>
              <p className="mt-1 text-sm text-indigo-100">
                Сатҳи шумо: <span className="font-bold text-white">{progress.level}</span>
              </p>
            </div>
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-white/20 text-xl font-extrabold">
              {progress.level}
            </div>
          </div>
          <div className="mt-5">
            <div className="mb-1 flex justify-between text-xs text-indigo-100">
              <span>Пешрафт</span>
              <span>{pct}%</span>
            </div>
            <div className="h-2.5 overflow-hidden rounded-full bg-white/25">
              <div
                className="h-full rounded-full bg-white transition-all duration-700"
                style={{ width: `${pct}%` }}
              />
            </div>
            <p className="mt-2 text-xs text-indigo-100">
              {progress.lessons_completed} аз {progress.lessons_total} дарс тамом шуд
            </p>
          </div>
        </div>

        {/* Омор */}
        <div className="grid grid-cols-3 gap-3">
          <StatCard
            value={progress.words_total}
            label="калима дар луғат"
            gradient="from-emerald-500 to-teal-600"
          />
          <StatCard
            value={progress.irregular_verbs}
            label="феъли номунтазам"
            gradient="from-amber-500 to-orange-600"
          />
          <StatCard
            value={progress.lessons_completed}
            label="дарси тамомшуда"
            gradient="from-sky-500 to-blue-600"
          />
        </div>

        {/* Тугмаҳои зуд */}
        <div className="grid gap-3 sm:grid-cols-2">
          <button
            onClick={() => onNavigate("lessons")}
            className="rounded-2xl border border-gray-200 bg-white p-5 text-left shadow-sm transition hover:shadow-md"
          >
            <div className="text-2xl">📖</div>
            <div className="mt-2 font-bold text-gray-800">Дарсҳои грамматика</div>
            <p className="mt-1 text-sm text-gray-500">Қоидаҳои A1–A2 бо шарҳи тоҷикӣ ва тест</p>
          </button>
          <button
            onClick={() => onNavigate("vocabulary")}
            className="rounded-2xl border border-gray-200 bg-white p-5 text-left shadow-sm transition hover:shadow-md"
          >
            <div className="text-2xl">🃏</div>
            <div className="mt-2 font-bold text-gray-800">Кортҳои луғат</div>
            <p className="mt-1 text-sm text-gray-500">Калимаҳо бо транскрипсия ва тарҷума</p>
          </button>
        </div>
      </div>
    </div>
  );
}
