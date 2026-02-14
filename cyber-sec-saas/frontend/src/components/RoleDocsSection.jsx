import React from "react";

const RoleDocsSection = () => (
  <section className="glass-bg py-12 px-8 text-center">
    <h2 className="text-3xl font-semibold mb-4">Role Documentation</h2>
    <ul className="flex flex-wrap justify-center gap-6 mt-4">
      <li className="glass-card p-4 rounded-lg">Super Admin</li>
      <li className="glass-card p-4 rounded-lg">Security Admin</li>
      <li className="glass-card p-4 rounded-lg">SOC Analyst</li>
      <li className="glass-card p-4 rounded-lg">Infra Admin</li>
      <li className="glass-card p-4 rounded-lg">Compliance Officer</li>
      <li className="glass-card p-4 rounded-lg">Auditor</li>
    </ul>
  </section>
);

export default RoleDocsSection;
