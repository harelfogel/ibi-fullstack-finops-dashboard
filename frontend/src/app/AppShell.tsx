"use client";

import { useState, createContext, useContext, useCallback, useEffect, type ReactNode } from "react";
import { usePathname, useRouter } from "next/navigation";
import { QueryProvider } from "@/lib/providers/QueryProvider";
import { ThemeProvider } from "@/lib/providers/ThemeProvider";
import { ToastProvider } from "@/lib/providers/ToastProvider";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopBar } from "@/components/layout/TopBar";
import { Footer } from "@/components/layout/Footer";
import { Modal } from "@/components/ui/Modal";
import { UploadContent } from "@/components/upload/UploadContent";

const UploadModalContext = createContext<{ openUploadModal: () => void }>({
  openUploadModal: () => {},
});

export function useUploadModal() {
  return useContext(UploadModalContext);
}

export function AppShell({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  const openUploadModal = useCallback(() => {
    setUploadModalOpen(true);
  }, []);

  // Close modal on route change
  useEffect(() => {
    setUploadModalOpen(false);
  }, [pathname]);

  const handleUploadSuccess = () => {
    setUploadModalOpen(false);
    router.push("/clients");
  };

  const isHome = pathname === "/";

  return (
    <ThemeProvider>
      <QueryProvider>
        <ToastProvider>
          <UploadModalContext.Provider value={{ openUploadModal }}>
            {isHome ? (
            <div className="flex h-screen flex-col overflow-hidden">
              <main className="flex-1 overflow-y-auto animate-fade-in">
                {children}
              </main>
            </div>
          ) : (
            <div className="flex h-screen overflow-hidden">
              <Sidebar
                open={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
                collapsed={collapsed}
                onToggleCollapse={() => setCollapsed((c) => !c)}
              />
              <div className="flex flex-1 flex-col overflow-hidden">
                <TopBar onMenuClick={() => setSidebarOpen(true)} />
                <main className="flex-1 overflow-y-auto p-6 animate-fade-in">
                  {children}
                </main>
                <Footer />
              </div>
            </div>
          )}

          <Modal open={uploadModalOpen} onClose={() => setUploadModalOpen(false)} title="Upload Transactions" size="lg">
            <UploadContent onSuccess={handleUploadSuccess} compact />
          </Modal>
          </UploadModalContext.Provider>
        </ToastProvider>
      </QueryProvider>
    </ThemeProvider>
  );
}
