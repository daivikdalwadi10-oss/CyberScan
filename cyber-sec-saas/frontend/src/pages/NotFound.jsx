export default function NotFound() {
  return (
    <div className="flex items-center justify-center min-h-screen flex-col gap-4">
      <div className="card p-8 max-w-md text-center">
        <h1 className="font-display text-2xl text-rose-300 mb-2">404 Not Found</h1>
        <p className="text-fog/70 mb-4">The page you are looking for does not exist.</p>
        <button
          onClick={() => window.location.href = "/"}
          className="bg-accent text-ink font-semibold rounded px-4 py-2 hover:brightness-110 transition"
        >
          Go Home
        </button>
      </div>
    </div>
  );
}