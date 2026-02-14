import React from "react";

const GettingStartedGuide = () => (
  <section className="glass-bg py-12 px-8 text-center">
    <h2 className="text-3xl font-semibold mb-4">Getting Started</h2>
    <ol className="list-decimal list-inside text-left mx-auto max-w-xl">
      <li>Clone the repository from GitHub.</li>
      <li>Run <span className="glass-code">docker-compose up --build</span> to start all services.</li>
      <li>Access the dashboard at <span className="glass-code">http://localhost:5173</span>.</li>
      <li>Login with provided credentials or create a new user.</li>
      <li>Monitor metrics in Grafana at <span className="glass-code">http://localhost:3000</span>.</li>
    </ol>
  </section>
);

export default GettingStartedGuide;
