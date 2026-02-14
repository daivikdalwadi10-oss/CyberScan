import React from "react";

const TechStackSection = () => (
  <section className="glass-bg py-12 px-8 text-center">
    <h2 className="text-3xl font-semibold mb-4">Technology Stack</h2>
    <ul className="flex flex-wrap justify-center gap-6 mt-4">
      <li className="glass-card p-4 rounded-lg">React + Vite</li>
      <li className="glass-card p-4 rounded-lg">FastAPI</li>
      <li className="glass-card p-4 rounded-lg">Postgres</li>
      <li className="glass-card p-4 rounded-lg">Docker Compose</li>
      <li className="glass-card p-4 rounded-lg">Prometheus</li>
      <li className="glass-card p-4 rounded-lg">Grafana</li>
    </ul>
  </section>
);

export default TechStackSection;
