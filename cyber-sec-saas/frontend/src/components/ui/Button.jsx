export default function Button({ variant = "primary", className = "", children, ...props }) {
  const base = "ripple-button inline-flex items-center justify-center rounded-full px-5 py-2 text-sm font-semibold transition";
  const styles = {
    primary: "bg-blue-500 text-white shadow-lg shadow-blue-500/30 hover:translate-y-[-1px]",
    secondary: "border border-white/15 text-[var(--color-text-primary)] hover:bg-white/10",
    ghost: "text-[var(--color-text-primary)] hover:bg-white/10"
  };

  return (
    <button className={`${base} ${styles[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}
