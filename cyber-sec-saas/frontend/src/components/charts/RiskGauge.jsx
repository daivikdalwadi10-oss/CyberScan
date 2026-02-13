import { RadialBarChart, RadialBar, PolarAngleAxis, ResponsiveContainer } from "recharts";

export default function RiskGauge({ value = 0 }) {
  const data = [{ name: "risk", value, fill: value > 70 ? "#ef4444" : value > 40 ? "#f59e0b" : "#10b981" }];

  return (
    <div className="h-56">
      <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart innerRadius="70%" outerRadius="90%" data={data} startAngle={180} endAngle={0}>
          <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
          <RadialBar dataKey="value" cornerRadius={10} />
        </RadialBarChart>
      </ResponsiveContainer>
      <div className="-mt-16 text-center">
        <p className="text-3xl font-display">{value}</p>
        <p className="text-xs text-[var(--color-text-muted)]">Risk Score</p>
      </div>
    </div>
  );
}
