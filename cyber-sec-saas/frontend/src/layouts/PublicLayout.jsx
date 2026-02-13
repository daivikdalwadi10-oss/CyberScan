import { Outlet } from "react-router-dom";
import Navbar from "../components/layout/Navbar.jsx";

export default function PublicLayout() {
  return (
    <div className="min-h-screen">
      <Navbar isPublic />
      <main className="px-6 pb-16 pt-10 lg:px-16">
        <Outlet />
      </main>
    </div>
  );
}
