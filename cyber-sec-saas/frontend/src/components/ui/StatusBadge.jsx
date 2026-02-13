const styles = {
  operational: "bg-emerald-500/15 text-emerald-200",
  warning: "bg-amber-500/20 text-amber-200",
  critical: "bg-red-500/20 text-red-200",
  info: "bg-blue-500/20 text-blue-200"
};

export default function StatusBadge({ status = "info", label }) {
  return (
    <span className={`badge ${styles[status] || styles.info}`}>
      {label || status}
    </span>
  );
}
