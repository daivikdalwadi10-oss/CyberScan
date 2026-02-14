import { createBrowserRouter, Navigate } from "react-router-dom";

import React, { Suspense, lazy } from "react";
import RoleGuard from "../components/layout/RoleGuard.jsx";
import ErrorBoundary from "../components/ErrorBoundary.jsx";

const AuthLayout = lazy(() => import("../layouts/AuthLayout.jsx"));
const DashboardLayout = lazy(() => import("../layouts/DashboardLayout.jsx"));
const PublicLayout = lazy(() => import("../layouts/PublicLayout.jsx"));

const Login = lazy(() => import("../pages/auth/Login.jsx"));
const ForgotPassword = lazy(() => import("../pages/auth/ForgotPassword.jsx"));

const PublicOverview = lazy(() => import("../pages/public/PublicOverview.jsx"));
const PublicIncidents = lazy(() => import("../pages/public/PublicIncidents.jsx"));
const PublicStatus = lazy(() => import("../pages/public/PublicStatus.jsx"));

const SuperAdminDashboard = lazy(() => import("../pages/Dashboard/superadmin/Index.jsx"));
const SecurityAdminDashboard = lazy(() => import("../pages/Dashboard/securityadmin/Index.jsx"));
const SocDashboard = lazy(() => import("../pages/Dashboard/soc/Index.jsx"));
const InfraDashboard = lazy(() => import("../pages/Dashboard/infra/Index.jsx"));
const ComplianceDashboard = lazy(() => import("../pages/Dashboard/compliance/Index.jsx"));
const AuditorDashboard = lazy(() => import("../pages/Dashboard/auditor/Index.jsx"));
const InternalUserDashboard = lazy(() => import("../pages/Dashboard/internaluser/Index.jsx"));
const DashboardIndex = lazy(() => import("../pages/Dashboard/DashboardIndex.jsx"));
const NotFound = lazy(() => import("../pages/NotFound.jsx"));
import { ROLES } from "../utils/roles.js";


const withSuspense = (element) => (
  <Suspense fallback={<div className="flex items-center justify-center min-h-screen">Loading...</div>}>
    <ErrorBoundary>{element}</ErrorBoundary>
  </Suspense>
);

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/public" replace />
  },
  {
    path: "/public",
    element: withSuspense(<PublicLayout />),
    children: [
      { index: true, element: withSuspense(<PublicOverview />) },
      { path: "status", element: withSuspense(<PublicStatus />) },
      { path: "incidents", element: withSuspense(<PublicIncidents />) }
    ]
  },
  {
    path: "/auth",
    element: withSuspense(<AuthLayout />),
    children: [
      { index: true, element: <Navigate to="login" replace /> },
      { path: "login", element: withSuspense(<Login />) },
      { path: "forgot", element: withSuspense(<ForgotPassword />) }
    ]
  },
  {
    path: "/dashboard",
    element: withSuspense(<DashboardLayout />),
    children: [
      {
        index: true,
        element: withSuspense(<DashboardIndex />)
      },
      {
        path: "superadmin",
        element: withSuspense(
          <RoleGuard allowedRoles={[ROLES.SuperAdmin]}>
            <SuperAdminDashboard />
          </RoleGuard>
        )
      },
      {
        path: "securityadmin",
        element: withSuspense(
          <RoleGuard allowedRoles={[ROLES.SecurityAdmin]}>
            <SecurityAdminDashboard />
          </RoleGuard>
        )
      },
      {
        path: "soc",
        element: withSuspense(
          <RoleGuard allowedRoles={[ROLES.SOCAnalyst]}>
            <SocDashboard />
          </RoleGuard>
        )
      },
      {
        path: "infra",
        element: withSuspense(
          <RoleGuard allowedRoles={[ROLES.InfraAdmin]}>
            <InfraDashboard />
          </RoleGuard>
        )
      },
      {
        path: "compliance",
        element: withSuspense(
          <RoleGuard allowedRoles={[ROLES.ComplianceOfficer]}>
            <ComplianceDashboard />
          </RoleGuard>
        )
      },
      {
        path: "auditor",
        element: withSuspense(
          <RoleGuard allowedRoles={[ROLES.Auditor]}>
            <AuditorDashboard />
          </RoleGuard>
        )
      },
      {
        path: "internaluser",
        element: withSuspense(
          <RoleGuard allowedRoles={[ROLES.InternalUser]}>
            <InternalUserDashboard />
          </RoleGuard>
        )
      }
    ]
  },
  {
    path: "*",
    element: withSuspense(<NotFound />)
  }
]);

export default router;
