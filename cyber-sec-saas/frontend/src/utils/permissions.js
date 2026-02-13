import { ROLES } from "./roles.js";

export const PERMISSIONS = {
  viewOverview: "viewOverview",
  viewAlerts: "viewAlerts",
  viewSystem: "viewSystem",
  viewRisk: "viewRisk",
  viewIncidents: "viewIncidents",
  viewAudit: "viewAudit",
  viewCloud: "viewCloud"
};

export const ROLE_PERMISSIONS = {
  [ROLES.SuperAdmin]: Object.values(PERMISSIONS),
  [ROLES.SecurityAdmin]: [
    PERMISSIONS.viewOverview,
    PERMISSIONS.viewAlerts,
    PERMISSIONS.viewRisk,
    PERMISSIONS.viewIncidents,
    PERMISSIONS.viewAudit
  ],
  [ROLES.SOCAnalyst]: [
    PERMISSIONS.viewOverview,
    PERMISSIONS.viewAlerts,
    PERMISSIONS.viewRisk,
    PERMISSIONS.viewIncidents
  ],
  [ROLES.InfraAdmin]: [
    PERMISSIONS.viewOverview,
    PERMISSIONS.viewSystem,
    PERMISSIONS.viewCloud
  ],
  [ROLES.ComplianceOfficer]: [
    PERMISSIONS.viewRisk,
    PERMISSIONS.viewIncidents,
    PERMISSIONS.viewAudit
  ],
  [ROLES.Auditor]: [PERMISSIONS.viewRisk, PERMISSIONS.viewAudit],
  [ROLES.InternalUser]: [PERMISSIONS.viewOverview]
};

export const hasPermission = (role, permission) => {
  if (!role) return false;
  const permissions = ROLE_PERMISSIONS[role] || [];
  return permissions.includes(permission);
};
