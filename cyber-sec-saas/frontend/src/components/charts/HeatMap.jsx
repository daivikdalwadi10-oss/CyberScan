const buildCells = (data) => {
  if (!data || data.length === 0) return [];
  return data.flatMap((row, rowIndex) =>
    row.map((value, colIndex) => ({
      id: `${rowIndex}-${colIndex}`,
      value
    }))
  );
};

export default function HeatMap({ data }) {
  const cells = buildCells(data);
  if (cells.length === 0) {
    return <div className="h-56 flex items-center justify-center text-sm text-[var(--color-text-muted)]">No data</div>;
  }

  return (
    <div className="grid grid-cols-8 gap-2">
      {cells.map((cell) => (
        <div
          key={cell.id}
          className="h-8 rounded-lg"
          style={{
            background: `rgba(239,68,68,${Math.min(0.8, 0.1 + cell.value / 10)})`
          }}
        />
      ))}
    </div>
  );
}
