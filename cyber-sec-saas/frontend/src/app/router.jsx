import { createBrowserRouter, Navigate } from "react-router-dom";

import AuthLayout from "../layouts/AuthLayout.jsx";
import DashboardLayout from "../layouts/DashboardLayout.jsx";
import PublicLayout from "../layouts/PublicLayout.jsx";

import Login from "../pages/auth/Login.jsx";
import ForgotPassword from "../pages/auth/ForgotPassword.jsx";

import PublicOverview from "../pages/public/PublicOverview.jsx";
import PublicIncidents from "../pages/public/PublicIncidents.jsx";
import PublicStatus from "../pages/public/PublicStatus.jsx";

import SuperAdminDashboard from "../pages/dashboard/superadmin/Index.jsx";
import SecurityAdminDashboard from "../pages/dashboard/securityadmin/Index.jsx";
import SocDashboard from "../pages/dashboard/soc/Index.jsx";
import InfraDashboard from "../pages/dashboard/infra/Index.jsx";
import ComplianceDashboard from "../pages/dashboard/compliance/Index.jsx";
import AuditorDashboard from "../pages/dashboard/auditor/Index.jsx";
import InternalUserDashboard from "../pages/dashboard/internaluser/Index.jsx";
import DashboardIndex from "../pages/dashboard/DashboardIndex.jsx";

import RoleGuard from "../components/layout/RoleGuard.jsx";
import { ROLES } from "../utils/roles.js";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/public" replace />
  },
  {
    path: "/public",
    element: <PublicLayout />,
    children: [
      { index: true, element: <PublicOverview /> },
      { path: "status", element: <PublicStatus /> },
      { path: "incidents", element: <PublicIncidents /> }
    ]
  },
  {
    path: "/auth",
    element: <AuthLayout />,
    children: [
      { index: true, element: <Navigate to="login" replace /> },
      { path: "login", element: <Login /> },
      { path: "forgot", element: <ForgotPassword /> }
    ]
  },
  {
    path: "/dashboard",
    element: <DashboardLayout />,
    children: [
      {
        index: true,
        element: <DashboardIndex />
      },
      {
        path: "superadmin",
        element: (
          <RoleGuard allowedRoles={[ROLES.SuperAdmin]}>
            <SuperAdminDashboard />
          </RoleGuard>
        )
      },
      {
        path: "securityadmin",
        element: (
          <RoleGuard allowedRoles={[ROLES.SecurityAdmin]}>
            <SecurityAdminDashboard />
          </RoleGuard>
        )
      },
      {
        path: "soc",
        element: (
          <RoleGuard allowedRoles={[ROLES.SOCAnalyst]}>
            <SocDashboard />
          </RoleGuard>
        )
      },
      {
        path: "infra",
        element: (
          <RoleGuard allowedRoles={[ROLES.InfraAdmin]}>
            <InfraDashboard />
          </RoleGuard>
        )
      },
      {
        path: "compliance",
        element: (
          <RoleGuard allowedRoles={[ROLES.ComplianceOfficer]}>
            <ComplianceDashboard />
          </RoleGuard>
        )
      },
      {
        path: "auditor",
        element: (
          <RoleGuard allowedRoles={[ROLES.Auditor]}>
            <AuditorDashboard />
          </RoleGuard>
        )
      },
      {
        path: "internaluser",
        element: (
          <RoleGuard allowedRoles={[ROLES.InternalUser]}>
            <InternalUserDashboard />
          </RoleGuard>
        )
      }
    ]
  },
  {
    path: "*",
    element: <Navigate to="/public" replace />
  }
]);

export default router;
