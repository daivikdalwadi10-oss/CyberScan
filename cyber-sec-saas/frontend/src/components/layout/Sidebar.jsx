import { NavLink } from "react-router-dom";
import { ShieldCheck, Activity, AlertTriangle, Cpu, Settings, FileText, BadgeAlert, Users, Radar, Cloud } from "lucide-react";
import { useRole } from "../../hooks/useRole.js";

const navByRole = {
  SuperAdmin: [
    { label: "Global Analytics", to: "/dashboard/superadmin", icon: Activity },
    { label: "User Management", to: "/dashboard/superadmin#users", icon: Users },
    { label: "Integrations", to: "/dashboard/superadmin#integrations", icon: Settings },
    { label: "Audit Timeline", to: "/dashboard/superadmin#audit", icon: FileText }
  ],
  SecurityAdmin: [
    { label: "Threat Intel", to: "/dashboard/securityadmin", icon: Radar },
    { label: "CVE Enrichment", to: "/dashboard/securityadmin#cves", icon: AlertTriangle },
    { label: "IOC Management", to: "/dashboard/securityadmin#ioc", icon: BadgeAlert },
    { label: "Escalation Rules", to: "/dashboard/securityadmin#rules", icon: Settings }
  ],
  SOCAnalyst: [
    { label: "Alert Board", to: "/dashboard/soc", icon: AlertTriangle },
    { label: "Incidents", to: "/dashboard/soc#incidents", icon: BadgeAlert },
    { label: "Lifecycle", to: "/dashboard/soc#lifecycle", icon: Activity }
  ],
  InfraAdmin: [
    { label: "Infrastructure", to: "/dashboard/infra", icon: Cpu },
    { label: "Dependencies", to: "/dashboard/infra#dependencies", icon: Activity },
    { label: "Cloud Status", to: "/dashboard/infra#cloud", icon: Cloud }
  ],
  ComplianceOfficer: [
    { label: "Risk Score", to: "/dashboard/compliance", icon: Activity },
    { label: "Audit Logs", to: "/dashboard/compliance#audit", icon: FileText },
    { label: "Reports", to: "/dashboard/compliance#reports", icon: ShieldCheck }
  ],
  Auditor: [
    { label: "Audit Explorer", to: "/dashboard/auditor", icon: FileText },
    { label: "Risk Comparison", to: "/dashboard/auditor#comparison", icon: Activity }
  ],
  InternalUser: [
    { label: "Availability", to: "/dashboard/internaluser", icon: Activity },
    { label: "My Activity", to: "/dashboard/internaluser#activity", icon: ShieldCheck }
  ]
};

export default function Sidebar() {
  const { role, label } = useRole();
  const items = navByRole[role] || navByRole.InternalUser;

  return (
    <aside className="hidden h-screen w-72 flex-col gap-6 border-r border-white/5 bg-white/5 px-6 py-6 shadow-2xl backdrop-blur-xl lg:flex">
      <div className="flex items-center gap-3">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-500/20 text-blue-200">
          <ShieldCheck size={22} />
        </div>
        <div>
          <p className="font-display text-lg">SentinelScope</p>
          <p className="text-xs text-[var(--color-text-muted)]">{label}</p>
        </div>
      </div>
      <nav className="flex flex-1 flex-col gap-2">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `nav-item nav-pill ${isActive ? "nav-item-active" : ""}`
              }
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
      <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-xs text-[var(--color-text-muted)]">
        Live operational data streaming every 30 seconds.
      </div>
    </aside>
  );
}
