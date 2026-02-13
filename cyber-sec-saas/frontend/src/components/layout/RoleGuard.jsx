import { Navigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth.js";
import { useRole } from "../../hooks/useRole.js";

export default function RoleGuard({ allowedRoles, children }) {
  const { isAuthenticated } = useAuth();
  const { role, defaultDashboardPath } = useRole();

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    return <Navigate to={defaultDashboardPath} replace />;
  }

  return children;
}
