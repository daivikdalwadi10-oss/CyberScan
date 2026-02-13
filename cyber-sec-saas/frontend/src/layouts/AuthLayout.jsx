import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-16">
      <div className="glass-panel w-full max-w-lg p-8">
        <Outlet />
      </div>
    </div>
  );
}
