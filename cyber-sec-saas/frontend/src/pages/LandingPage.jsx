import React from "react";
import HeroSection from "../components/HeroSection";
import ProductOverview from "../components/ProductOverview";
import ArchitectureSection from "../components/ArchitectureSection";
import SecurityOverview from "../components/SecurityOverview";
import LiveMetricsPreview from "../components/LiveMetricsPreview";
import TechStackSection from "../components/TechStackSection";
import MonitoringStackInfo from "../components/MonitoringStackInfo";
import RoleDocsSection from "../components/RoleDocsSection";
import GettingStartedGuide from "../components/GettingStartedGuide";
import Footer from "../components/Footer";

const LandingPage = () => {
  return (
    <div className="glass-bg min-h-screen flex flex-col">
      <HeroSection />
      <ProductOverview />
      <ArchitectureSection />
      <SecurityOverview />
      <LiveMetricsPreview />
      <TechStackSection />
      <MonitoringStackInfo />
      <RoleDocsSection />
      <GettingStartedGuide />
      <Footer />
    </div>
  );
};

export default LandingPage;
