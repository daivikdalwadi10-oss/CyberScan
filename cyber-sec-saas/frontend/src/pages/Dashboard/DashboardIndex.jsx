import { Navigate } from "react-router-dom";
import { useRole } from "../../hooks/useRole.js";

export default function DashboardIndex() {
  const { defaultDashboardPath } = useRole();
  return <Navigate to={defaultDashboardPath} replace />;
}
