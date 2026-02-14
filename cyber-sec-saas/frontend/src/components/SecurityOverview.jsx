import React from "react";

const SecurityOverview = () => (
  <section className="glass-bg py-12 px-8 text-center">
    <h2 className="text-3xl font-semibold mb-4">Security Overview</h2>
    <p className="text-lg mb-2">Multi-role RBAC, JWT authentication, encrypted data, audit logging, compliance automation.</p>
    <ul className="flex flex-wrap justify-center gap-6 mt-4">
      <li className="glass-card p-4 rounded-lg">Role-Based Access</li>
      <li className="glass-card p-4 rounded-lg">Audit Logging</li>
      <li className="glass-card p-4 rounded-lg">Compliance Automation</li>
      <li className="glass-card p-4 rounded-lg">Secure API Gateway</li>
      <li className="glass-card p-4 rounded-lg">Data Encryption</li>
    </ul>
  </section>
);

export default SecurityOverview;
