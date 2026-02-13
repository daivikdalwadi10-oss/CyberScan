import { useEffect, useState } from "react";
import GlassCard from "../ui/GlassCard.jsx";
import LineChart from "../charts/LineChart.jsx";
import { getPublicStatus } from "../../services/api.js";

export default function UptimeWidget() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    getPublicStatus()
      .then((data) => {
        if (isMounted) setHistory(data?.uptimeHistory || []);
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load uptime history");
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <GlassCard className="flex flex-col gap-4">
      <div>
        <p className="text-sm font-semibold">Uptime Trend</p>
        <p className="text-xs text-[var(--color-text-muted)]">Last 7 months</p>
      </div>
      {error ? <p className="text-sm text-red-200">{error}</p> : null}
      <LineChart data={history} xKey="month" yKey="uptime" stroke="#3b82f6" />
    </GlassCard>
  );
}
