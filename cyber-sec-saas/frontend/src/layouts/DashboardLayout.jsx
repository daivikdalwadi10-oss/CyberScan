import { Outlet } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar.jsx";
import Navbar from "../components/layout/Navbar.jsx";

export default function DashboardLayout() {
  return (
    <div className="min-h-screen flex bg-transparent">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar />
        <main className="flex-1 overflow-hidden">
          <div className="h-full overflow-y-auto px-6 pb-10 pt-6 lg:px-10">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
