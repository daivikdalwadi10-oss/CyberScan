import React from "react";

const MonitoringStackInfo = () => (
  <section className="glass-bg py-12 px-8 text-center">
    <h2 className="text-3xl font-semibold mb-4">Monitoring Stack</h2>
    <ul className="flex flex-wrap justify-center gap-6 mt-4">
      <li className="glass-card p-4 rounded-lg">Prometheus Metrics</li>
      <li className="glass-card p-4 rounded-lg">Grafana Dashboards</li>
      <li className="glass-card p-4 rounded-lg">Live API Monitoring</li>
      <li className="glass-card p-4 rounded-lg">System Health Checks</li>
    </ul>
  </section>
);

export default MonitoringStackInfo;
