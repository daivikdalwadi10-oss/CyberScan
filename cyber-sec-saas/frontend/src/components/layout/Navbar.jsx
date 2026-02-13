import { Link, useNavigate } from "react-router-dom";
import { Bell, LogOut, Moon, Sun } from "lucide-react";
import { useAuth } from "../../hooks/useAuth.js";
import { useTheme } from "../../theme/ThemeProvider.jsx";
import Button from "../ui/Button.jsx";

export default function Navbar({ isPublic = false }) {
  const { user, role, logout, isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/auth/login", { replace: true });
  };

  return (
    <header className="sticky top-0 z-20 border-b border-white/10 bg-white/5 backdrop-blur-xl">
      <div className="mx-auto flex max-w-[1400px] items-center justify-between px-6 py-4 lg:px-10">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-[var(--color-text-muted)]">Security Operations</p>
          <h1 className="font-display text-2xl">Enterprise Command Center</h1>
        </div>
        <div className="flex items-center gap-3">
          <button className="icon-button ripple-button" onClick={toggleTheme} type="button" aria-label="Toggle theme">
            {theme === "dark" ? <Sun size={16} /> : <Moon size={16} />}
          </button>
          {!isPublic && isAuthenticated ? (
            <>
              <button className="icon-button ripple-button" type="button" aria-label="Notifications">
                <Bell size={16} />
              </button>
              <div className="glass-card flex items-center gap-3 px-4 py-2">
                <div>
                  <p className="text-sm">{user?.full_name || user?.email || "Analyst"}</p>
                  <p className="text-xs text-[var(--color-text-muted)]">{role || "InternalUser"}</p>
                </div>
                <button className="icon-button ripple-button" type="button" onClick={handleLogout} aria-label="Logout">
                  <LogOut size={14} />
                </button>
              </div>
            </>
          ) : (
            <Link to="/auth/login">
              <Button>Sign In</Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
