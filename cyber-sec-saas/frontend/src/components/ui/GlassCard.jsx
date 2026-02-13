export default function GlassCard({ className = "", children }) {
  return <div className={`glass-card p-6 ${className}`}>{children}</div>;
}
