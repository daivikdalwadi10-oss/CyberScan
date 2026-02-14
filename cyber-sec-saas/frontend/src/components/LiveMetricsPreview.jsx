import React from "react";

const LiveMetricsPreview = () => (
  <section className="glass-bg py-12 px-8 text-center">
    <h2 className="text-3xl font-semibold mb-4">Live Public Metric Preview</h2>
    <div className="flex flex-wrap justify-center gap-6 mt-4">
      <div className="glass-card p-4 rounded-lg">
        <span className="text-2xl font-bold">Uptime</span>
        <div className="text-lg">99.99%</div>
      </div>
      <div className="glass-card p-4 rounded-lg">
        <span className="text-2xl font-bold">API Response Time</span>
        <div className="text-lg">120ms</div>
      </div>
      <div className="glass-card p-4 rounded-lg">
        <span className="text-2xl font-bold">Security Alerts</span>
        <div className="text-lg">3</div>
      </div>
      <div className="glass-card p-4 rounded-lg">
        <span className="text-2xl font-bold">System Health</span>
        <div className="text-lg">Healthy</div>
      </div>
    </div>
  </section>
);

export default LiveMetricsPreview;
