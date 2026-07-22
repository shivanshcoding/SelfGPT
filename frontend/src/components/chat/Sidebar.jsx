"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, MessageSquare, PanelLeftClose, PanelLeft, Settings, LogOut, Search, Brain } from "lucide-react";
import useSidebarStore from "@/stores/sidebarStore";
import useAuthStore from "@/stores/authStore";
import { cn } from "@/lib/utils";
import Logo from "@/components/common/Logo";

export function Sidebar() {
  const { isOpen, toggle } = useSidebarStore();
  const { user, clearAuth } = useAuthStore();
  const params = useParams();
  const activeChatId = params?.chatId;

  // Placeholder for real chats
  const chats = [
    { id: "1", title: "Stoicism vs Modern Life", identity: "marcus-aurelius" },
    { id: "2", title: "Debugging React State", identity: "senior-dev" },
  ];

  return (
    <>
      <AnimatePresence>
        {isOpen && (
          <motion.aside
            initial={{ x: "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: "-100%" }}
            transition={{ type: "spring", bounce: 0, duration: 0.3 }}
            className="fixed inset-y-0 left-0 z-40 w-[var(--sidebar-width)] bg-[var(--color-bg-secondary)] border-r border-[var(--color-border)] flex flex-col"
          >
            {/* Header */}
            <div className="p-4 flex items-center justify-between">
              <Link href="/chat" className="flex items-center gap-2">
                <Logo size="small" />
              </Link>
              <button 
                onClick={toggle}
                className="p-2 rounded-lg hover:bg-[var(--color-surface)] text-[var(--color-text-secondary)] transition-colors"
                aria-label="Close sidebar"
              >
                <PanelLeftClose size={20} />
              </button>
            </div>

            {/* New Chat Button */}
            <div className="px-4 pb-4">
              <Link
                href="/chat"
                className="flex items-center gap-2 w-full p-3 rounded-xl bg-[var(--color-surface)] hover:bg-[var(--color-surface-hover)] border border-[var(--color-border)] transition-colors font-medium"
              >
                <Plus size={20} />
                <span>New chat</span>
              </Link>
            </div>

            {/* Search */}
            <div className="px-4 pb-2">
              <div className="relative">
                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)]" />
                <input 
                  type="text"
                  placeholder="Search chats..."
                  className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg py-2 pl-9 pr-3 text-sm focus:outline-none focus:border-[var(--color-accent)] transition-colors"
                />
              </div>
            </div>

            {/* Chat List */}
            <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1 scrollbar-hide">
              <Link
                href="/memories"
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors group mb-4",
                  "text-[var(--color-text-secondary)] hover:bg-[var(--color-surface)]"
                )}
              >
                <Brain size={16} className="text-[var(--color-accent)]" />
                <span className="truncate flex-1 font-medium text-[var(--color-text)]">Memory Vault</span>
              </Link>
              
              <div className="px-3 mb-2 text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider">
                Recent Chats
              </div>
              {chats.map((chat) => (
                <Link
                  key={chat.id}
                  href={`/chat/${chat.id}`}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors group",
                    activeChatId === chat.id 
                      ? "bg-[var(--color-surface-active)] text-[var(--color-text)] font-medium" 
                      : "text-[var(--color-text-secondary)] hover:bg-[var(--color-surface)]"
                  )}
                >
                  <MessageSquare size={16} className={activeChatId === chat.id ? "text-[var(--color-accent)]" : "text-[var(--color-text-muted)] group-hover:text-[var(--color-text-secondary)]"} />
                  <span className="truncate flex-1">{chat.title}</span>
                </Link>
              ))}
            </div>

            {/* User Footer */}
            <div className="p-4 border-t border-[var(--color-border)]">
              <div className="flex items-center gap-3 w-full p-2 rounded-xl hover:bg-[var(--color-surface)] transition-colors cursor-pointer group">
                <div className="w-8 h-8 rounded-full bg-[var(--color-accent)] flex items-center justify-center text-white font-bold uppercase">
                  {user?.username?.charAt(0) || "U"}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{user?.username || "User"}</p>
                  <p className="text-xs text-[var(--color-text-muted)] truncate">{user?.email || ""}</p>
                </div>
                <button 
                  onClick={(e) => { e.preventDefault(); clearAuth(); window.location.href='/login'; }}
                  className="p-1.5 text-[var(--color-text-muted)] hover:text-[var(--color-error)] opacity-0 group-hover:opacity-100 transition-all rounded-md hover:bg-[var(--color-error)]/10"
                  title="Logout"
                >
                  <LogOut size={16} />
                </button>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Floating Toggle Button (when sidebar is closed) */}
      {!isOpen && (
        <button
          onClick={toggle}
          className="fixed top-4 left-4 z-40 p-2 rounded-lg bg-[var(--color-bg)] border border-[var(--color-border)] shadow-sm hover:bg-[var(--color-surface)] text-[var(--color-text-secondary)] transition-all"
          aria-label="Open sidebar"
        >
          <PanelLeft size={20} />
        </button>
      )}
    </>
  );
}
