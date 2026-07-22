"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";
import { Brain, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { formatDate } from "@/lib/utils";

export default function MemoriesPage() {
  const [memories, setMemories] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchMemories = async () => {
    try {
      const res = await api.get("/api/memories/");
      setMemories(res.data);
    } catch (err) {
      toast.error("Failed to load memories.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMemories();
  }, []);

  const handleDelete = async (id) => {
    try {
      await api.delete(`/api/memories/${id}`);
      setMemories((prev) => prev.filter((m) => m.id !== id));
      toast.success("Memory forgotten.");
    } catch (err) {
      toast.error("Failed to forget memory.");
    }
  };

  return (
    <div className="flex-1 p-6 md:p-12 overflow-y-auto bg-[var(--color-bg)]">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-[var(--color-accent)]/10 flex items-center justify-center text-[var(--color-accent)]">
            <Brain size={24} />
          </div>
          <div>
            <h1 className="text-display font-semibold text-[var(--color-text)]">
              Memories
            </h1>
            <p className="text-body text-[var(--color-text-secondary)]">
              Facts and preferences SelfGPT has learned about you across conversations.
            </p>
          </div>
        </div>

        {isLoading ? (
          <div className="text-[var(--color-text-muted)]">Loading memories...</div>
        ) : memories.length === 0 ? (
          <div className="p-8 text-center border border-dashed border-[var(--color-border)] rounded-2xl bg-[var(--color-surface)]">
            <p className="text-[var(--color-text-secondary)]">No memories found yet. Start chatting and SelfGPT will learn about you!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {memories.map((mem, i) => (
              <motion.div
                key={mem.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: i * 0.05 }}
                className="p-4 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] hover:shadow-sm transition-shadow flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-[var(--color-accent-soft)] text-[var(--color-accent-hover)] uppercase tracking-wider">
                      {mem.memory_type.replace("_", " ")}
                    </span>
                    <button
                      onClick={() => handleDelete(mem.id)}
                      className="p-1.5 text-[var(--color-text-muted)] hover:text-[var(--color-error)] hover:bg-[var(--color-error)]/10 rounded-md transition-colors"
                      title="Forget this memory"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                  <p className="text-[var(--color-text)] leading-relaxed">
                    "{mem.content}"
                  </p>
                </div>
                <div className="mt-4 pt-4 border-t border-[var(--color-border)] text-xs text-[var(--color-text-muted)] flex justify-between">
                  <span>Learned on {formatDate(mem.created_at)}</span>
                  <span>{mem.identity_id ? `via ${mem.identity_id}` : "Global"}</span>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
