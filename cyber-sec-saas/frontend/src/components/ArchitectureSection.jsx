import React from "react";

const ArchitectureSection = () => (
  <section className="glass-bg py-12 px-8 text-center">
    <h2 className="text-3xl font-semibold mb-4">Architecture</h2>
    <p className="text-lg mb-2">Microservices, containerized deployment, scalable backend, secure frontend, integrated monitoring.</p>
    <div className="flex justify-center mt-6">
      <img src="/architecture-diagram.png" alt="Architecture Diagram" className="glass-img rounded-xl shadow-lg" style={{maxWidth: '600px'}} />
    </div>
  </section>
);

export default ArchitectureSection;
