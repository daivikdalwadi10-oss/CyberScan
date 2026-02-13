import { Component } from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-screen flex-col gap-4">
          <div className="card p-8 max-w-md text-center">
            <h1 className="font-display text-2xl text-rose-300 mb-2">Error</h1>
            <p className="text-fog/70 mb-4">{this.state.error?.message || "Something went wrong"}</p>
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

    return this.props.children;
  }
}
