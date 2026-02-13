export default function DataTable({ columns, rows, emptyMessage = "No records available." }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="glass-card p-6 text-sm text-[var(--color-text-muted)]">{emptyMessage}</div>
    );
  }

  return (
    <div className="glass-card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-white/5 text-xs uppercase tracking-[0.3em] text-[var(--color-text-muted)]">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className="px-4 py-3">
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id || JSON.stringify(row)} className="border-t border-white/5">
                {columns.map((column) => (
                  <td key={column.key} className="px-4 py-3 text-[var(--color-text-primary)]">
                    {column.render ? column.render(row) : row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
