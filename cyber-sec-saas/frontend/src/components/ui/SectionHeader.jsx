export default function SectionHeader({ eyebrow, title, description, action }) {
  return (
    <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
      <div>
        {eyebrow ? (
          <p className="text-xs uppercase tracking-[0.4em] text-blue-300/70">{eyebrow}</p>
        ) : null}
        <h2 className="font-display text-2xl">{title}</h2>
        {description ? (
          <p className="mt-2 text-sm text-[var(--color-text-muted)]">{description}</p>
        ) : null}
      </div>
      {action ? <div>{action}</div> : null}
    </div>
  );
}
