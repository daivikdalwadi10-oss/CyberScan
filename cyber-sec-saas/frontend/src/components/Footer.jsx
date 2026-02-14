import React from "react";

const Footer = () => (
  <footer className="glass-bg py-8 px-8 text-center mt-auto">
    <div className="flex flex-wrap justify-center gap-6 mb-4">
      <a href="https://github.com/your-org/cybersec-platform" className="glass-link">GitHub</a>
      <a href="/docs" className="glass-link">Documentation</a>
      <a href="/monitoring" className="glass-link">Monitoring</a>
      <a href="/roles" className="glass-link">Roles</a>
      <a href="/deployment" className="glass-link">Deployment</a>
    </div>
    <div className="text-sm text-glass">&copy; 2026 CyberSec Platform. All rights reserved.</div>
  </footer>
);

export default Footer;
