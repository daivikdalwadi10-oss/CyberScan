import { useEffect, useMemo, useState } from "react";
import GlassCard from "./GlassCard.jsx";

const animateValue = (start, end, duration, callback) => {
  const startTime = performance.now();
  const step = (now) => {
    const progress = Math.min((now - startTime) / duration, 1);
    const value = start + (end - start) * progress;
    callback(value);
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
};

const accentColors = {
  blue: "text-blue-200",
  emerald: "text-emerald-200",
  amber: "text-amber-200",
  red: "text-red-200"
};

export default function MetricCard({ label, value, unit, accent = "blue", delta, isLoading, error }) {
  const [animatedValue, setAnimatedValue] = useState(0);
  const numericValue = useMemo(() => (typeof value === "number" ? value : Number(value || 0)), [value]);

  useEffect(() => {
    if (Number.isNaN(numericValue)) return;
    animateValue(0, numericValue, 800, setAnimatedValue);
  }, [numericValue]);

  return (
    <GlassCard className="flex flex-col gap-3 min-h-[140px]">
      <p className="text-xs uppercase tracking-[0.3em] text-[var(--color-text-muted)]">{label}</p>
      {isLoading ? (
        <div className="h-10 w-32 rounded-full skeleton" />
      ) : error ? (
        <p className="text-sm text-red-200">{error}</p>
      ) : (
        <div className="flex items-baseline gap-2">
          <span className={`text-3xl font-display ${accentColors[accent] || accentColors.blue}`}>
            {animatedValue.toFixed(0)}
          </span>
          {unit ? <span className="text-sm text-[var(--color-text-muted)]">{unit}</span> : null}
        </div>
      )}
      {delta ? <p className="text-xs text-emerald-200">{delta}</p> : null}
    </GlassCard>
  );
}
