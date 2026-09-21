import { useState, type ReactNode } from "react";
import { useAuth } from "../contexts/AuthContext";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";

interface AppLayoutProps {
  children: ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  const { user } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Для гостя — только Navbar + контент
  if (!user) {
    return (
      <div className="min-h-screen">
        <Navbar />
        <main>{children}</main>
      </div>
    );
  }

  // Для авторизованного — Navbar + Sidebar + контент
  return (
    <div className="min-h-screen">
      <Navbar onMenuClick={() => setSidebarOpen(true)} />

      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Контент с отступом слева под sidebar */}
      <main className="lg:pl-64 pt-0 min-h-[calc(100vh-4rem)]">
        {children}
      </main>
    </div>
  );
}