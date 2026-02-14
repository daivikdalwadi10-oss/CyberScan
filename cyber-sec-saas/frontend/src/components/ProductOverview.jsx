import React from "react";

const ProductOverview = () => (
  <section className="glass-bg py-12 px-8 text-center">
    <h2 className="text-3xl font-semibold mb-4">Product Overview</h2>
    <p className="text-lg mb-2">Unified dashboard, real-time metrics, role-based access, and advanced threat intelligence.</p>
    <ul className="flex flex-wrap justify-center gap-6 mt-4">
      <li className="glass-card p-4 rounded-lg">Live Security Metrics</li>
      <li className="glass-card p-4 rounded-lg">Role-Based Dashboards</li>
      <li className="glass-card p-4 rounded-lg">Prometheus & Grafana Monitoring</li>
      <li className="glass-card p-4 rounded-lg">Enterprise Authentication</li>
      <li className="glass-card p-4 rounded-lg">Automated Compliance</li>
    </ul>
  </section>
);

export default ProductOverview;
