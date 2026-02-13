import Button from "../../components/ui/Button.jsx";

export default function ForgotPassword() {
  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs uppercase tracking-[0.4em] text-blue-300/70">Account Recovery</p>
        <h2 className="font-display text-3xl">Reset access</h2>
        <p className="mt-2 text-sm text-[var(--color-text-muted)]">
          Password resets are managed by your enterprise identity provider.
        </p>
      </div>
      <Button variant="secondary" onClick={() => window.history.back()}>Return to Sign In</Button>
    </div>
  );
}
