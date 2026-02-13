import { useMemo } from "react";
import { useAuth } from "./useAuth.js";

export const roleConfig = {
  SuperAdmin: { label: "Super Admin", path: "/dashboard/superadmin" },
  SecurityAdmin: { label: "Security Admin", path: "/dashboard/securityadmin" },
  SOCAnalyst: { label: "SOC Analyst", path: "/dashboard/soc" },
  InfraAdmin: { label: "Infrastructure Admin", path: "/dashboard/infra" },
  ComplianceOfficer: { label: "Compliance Officer", path: "/dashboard/compliance" },
  Auditor: { label: "Auditor", path: "/dashboard/auditor" },
  InternalUser: { label: "Internal User", path: "/dashboard/internaluser" }
};

export const getRolePath = (role) => (roleConfig[role] || roleConfig.InternalUser).path;

export const useRole = () => {
  const { role } = useAuth();

  return useMemo(() => {
    const config = roleConfig[role] || roleConfig.InternalUser;
    return {
      role: role || "InternalUser",
      label: config.label,
      defaultDashboardPath: config.path
    };
  }, [role]);
};
