const styles = {
  critical: "badge badge-critical",
  high: "badge badge-high",
  medium: "badge badge-medium",
  low: "badge badge-low"
};

export default function Badge({ tone = "low", children }) {
  const className = styles[tone] || styles.low;
  return <span className={className}>{children}</span>;
}
