import GlassCard from "./GlassCard.jsx";

export default function StatCard({ label, value, trend }) {
  return (
    <GlassCard className="p-5">
      <p className="text-xs uppercase tracking-[0.2em] text-fog/60">{label}</p>
      <p className="mt-3 text-3xl font-display">{value}</p>
      {trend ? <p className="mt-2 text-sm text-fog/70">{trend}</p> : null}
    </GlassCard>
  );
}
