import { LineChart as ReLineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function LineChart({ data, xKey, yKey, stroke = "#3b82f6" }) {
  if (!data || data.length === 0) {
    return <div className="h-56 flex items-center justify-center text-sm text-[var(--color-text-muted)]">No data</div>;
  }

  return (
    <div className="h-56">
      <ResponsiveContainer width="100%" height="100%">
        <ReLineChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
          <XAxis dataKey={xKey} stroke="rgba(226,232,240,0.5)" />
          <YAxis stroke="rgba(226,232,240,0.5)" />
          <Tooltip contentStyle={{ background: "rgba(15,23,42,0.9)", border: "1px solid rgba(255,255,255,0.1)" }} />
          <Line type="monotone" dataKey={yKey} stroke={stroke} strokeWidth={2} dot={false} />
        </ReLineChart>
      </ResponsiveContainer>
    </div>
  );
}
