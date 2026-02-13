import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../../components/ui/Button.jsx";
import { login as loginRequest } from "../../services/auth.js";
import { useAuth } from "../../hooks/useAuth.js";
import { getRolePath } from "../../hooks/useRole.js";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setSession } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await loginRequest({ email, password });
      setSession({
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
        role: data.user?.roles?.[0],
        user: data.user
      });
      navigate(getRolePath(data.user?.roles?.[0]), { replace: true });
    } catch (err) {
      setError(err?.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.4em] text-blue-300/70">Secure Access</p>
        <h2 className="font-display text-3xl">Sign in to SentinelScope</h2>
        <p className="mt-2 text-sm text-[var(--color-text-muted)]">
          Access your role-based command center with live telemetry.
        </p>
      </div>
      <form className="space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="text-xs uppercase tracking-[0.3em] text-[var(--color-text-muted)]">Email</label>
          <input className="input-field mt-2" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label className="text-xs uppercase tracking-[0.3em] text-[var(--color-text-muted)]">Password</label>
          <input className="input-field mt-2" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        {error ? <p className="text-sm text-red-200">{error}</p> : null}
        <Button className="w-full" type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Sign In"}
        </Button>
      </form>
      <div className="text-sm text-[var(--color-text-muted)]">
        Forgot password? Contact your security administrator.
      </div>
    </div>
  );
}
