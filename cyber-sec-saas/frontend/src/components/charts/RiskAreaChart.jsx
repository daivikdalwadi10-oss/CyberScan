import {
  Area,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

const defaultData = [
  { name: "Mon", score: 42 },
  { name: "Tue", score: 55 },
  { name: "Wed", score: 62 },
  { name: "Thu", score: 58 },
  { name: "Fri", score: 68 },
  { name: "Sat", score: 71 },
  { name: "Sun", score: 64 }
];

export default function RiskAreaChart({ data = defaultData }) {
  return (
    <div className="h-56 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ left: 0, right: 0, top: 10, bottom: 0 }}>
          <defs>
            <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#00F5D4" stopOpacity={0.55} />
              <stop offset="100%" stopColor="#00F5D4" stopOpacity={0.05} />
            </linearGradient>
          </defs>
          <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: "#94a3b8" }} />
          <YAxis axisLine={false} tickLine={false} tick={{ fill: "#94a3b8" }} />
          <Tooltip
            contentStyle={{ background: "#0b1220", border: "1px solid #1f2937" }}
            labelStyle={{ color: "#e2e8f0" }}
          />
          <Area
            type="monotone"
            dataKey="score"
            stroke="#00F5D4"
            strokeWidth={2}
            fill="url(#riskGradient)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
