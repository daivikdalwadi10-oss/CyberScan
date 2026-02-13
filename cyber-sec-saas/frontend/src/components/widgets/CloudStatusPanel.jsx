import { useEffect, useState } from "react";
import GlassCard from "../ui/GlassCard.jsx";
import StatusBadge from "../ui/StatusBadge.jsx";
import { getPublicStatus } from "../../services/api.js";

export default function CloudStatusPanel() {
  const [services, setServices] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    getPublicStatus()
      .then((data) => {
        if (isMounted) setServices(data?.cloudStatus || []);
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load cloud status");
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <GlassCard className="flex flex-col gap-4">
      <div>
        <p className="text-sm font-semibold">Cloud Provider Status</p>
        <p className="text-xs text-[var(--color-text-muted)]">Live provider signals</p>
      </div>
      {error ? <p className="text-sm text-red-200">{error}</p> : null}
      <div className="space-y-3">
        {services.length === 0 ? (
          <p className="text-sm text-[var(--color-text-muted)]">No provider updates.</p>
        ) : (
          services.map((service) => (
            <div key={`${service.provider}-${service.service}-${service.region}`} className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              <div>
                <p className="text-sm">{service.provider} · {service.service}</p>
                <p className="text-xs text-[var(--color-text-muted)]">{service.region}</p>
              </div>
              <StatusBadge status={service.status === "operational" ? "operational" : "warning"} label={service.status} />
            </div>
          ))
        )}
      </div>
    </GlassCard>
  );
}
