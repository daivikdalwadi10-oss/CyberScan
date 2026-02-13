import { AreaChart as ReAreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function AreaChart({ data, xKey, yKey, stroke = "#10b981", fill = "rgba(16,185,129,0.2)" }) {
  if (!data || data.length === 0) {
    return <div className="h-56 flex items-center justify-center text-sm text-[var(--color-text-muted)]">No data</div>;
  }

  return (
    <div className="h-56">
      <ResponsiveContainer width="100%" height="100%">
        <ReAreaChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
          <XAxis dataKey={xKey} stroke="rgba(226,232,240,0.5)" />
          <YAxis stroke="rgba(226,232,240,0.5)" />
          <Tooltip contentStyle={{ background: "rgba(15,23,42,0.9)", border: "1px solid rgba(255,255,255,0.1)" }} />
          <Area type="monotone" dataKey={yKey} stroke={stroke} fill={fill} strokeWidth={2} />
        </ReAreaChart>
      </ResponsiveContainer>
    </div>
  );
}
