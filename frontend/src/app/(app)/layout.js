import { Sidebar } from "@/components/chat/Sidebar";

export default function AppLayout({ children }) {
  return (
    <div className="flex h-screen bg-[var(--color-bg)] overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 relative h-full">
        {children}
      </main>
    </div>
  );
}
