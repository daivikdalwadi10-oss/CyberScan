import { useEffect, useState } from "react";
import { useAuth } from "../../hooks/useAuth.js";
import { fetchRoleDocs } from "../../services/api.js";
import GlassCard from "../../components/ui/GlassCard.jsx";

export default function DocumentationPanel() {
  const { role } = useAuth();
  const [guide, setGuide] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchRoleDocs(role)
      .then((data) => {
        setGuide(data.guide || "No documentation found for this role.");
        setError(null);
      })
      .catch((err) => {
        setError("Failed to load documentation.");
        setGuide("");
      })
      .finally(() => setLoading(false));
  }, [role]);

  return (
    <GlassPanel title="Role-Based Documentation" style={{ minHeight: 300 }}>
      {loading ? (
        <div>Loading...</div>
      ) : error ? (
        <div style={{ color: "#e57373" }}>{error}</div>
      ) : (
        <div dangerouslySetInnerHTML={{ __html: guide.replace(/\n/g, "<br />") }} />
      )}
    </GlassPanel>
  );
}
