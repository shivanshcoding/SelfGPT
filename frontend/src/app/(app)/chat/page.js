"use client";

import { motion } from "framer-motion";
import { IDENTITY_CATEGORIES } from "@/lib/constants";
import { Card, CardContent } from "@/components/ui/card";
import { Plus } from "lucide-react";
import Logo from "@/components/common/Logo";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

export default function ChatEmptyState() {
  const router = useRouter();
  const [identities, setIdentities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchIdentities() {
      try {
        const res = await api.get("/api/identities/");
        setIdentities(res.data.identities);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchIdentities();
  }, []);

  const handleStartChat = async (identity) => {
    try {
      const res = await api.post("/api/chats/", {
        identity_id: identity.slug,
        title: `Chat with ${identity.name}`
      });
      router.push(`/chat/${res.data.id}`);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 bg-[var(--color-bg)] overflow-y-auto">
      <div className="max-w-4xl w-full space-y-12 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center space-y-6"
        >
          <div className="flex justify-center mb-6">
            <Logo size="hero" />
          </div>
          <h1 className="text-display font-semibold text-[var(--color-text)]">
            Who do you want to talk to?
          </h1>
          <p className="text-body text-[var(--color-text-secondary)]">
            Select an identity to start a conversation, or create your own custom AI.
          </p>
        </motion.div>

        {isLoading ? (
          <div className="text-center">Loading identities...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Create Custom Card */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4 }}
              onClick={() => router.push("/identities/new")}
            >
              <Card className="h-full border-dashed border-2 hover:border-[var(--color-accent)] cursor-pointer transition-colors bg-transparent group">
                <CardContent className="p-6 flex flex-col items-center justify-center h-full space-y-4 min-h-[200px]">
                  <div className="w-12 h-12 rounded-full bg-[var(--color-surface)] group-hover:bg-[var(--color-accent)] flex items-center justify-center transition-colors">
                    <Plus className="text-[var(--color-text-secondary)] group-hover:text-white" />
                  </div>
                  <div className="text-center">
                    <h3 className="font-semibold text-[var(--color-text)]">Create Custom</h3>
                    <p className="text-sm text-[var(--color-text-muted)]">Build your own identity</p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Existing Identities */}
            {identities.map((identity, i) => {
              const category = Object.values(IDENTITY_CATEGORIES).find(c => c.label.toLowerCase() === identity.category.toLowerCase()) || IDENTITY_CATEGORIES.CUSTOM;
              
              return (
                <motion.div
                  key={identity.id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: (i + 1) * 0.05 }}
                  onClick={() => handleStartChat(identity)}
                >
                  <Card className="h-full border-transparent hover:border-[var(--color-accent)]/30 hover:shadow-md cursor-pointer transition-all bg-[var(--color-surface)] group relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-[var(--color-accent)]/10 to-transparent rounded-bl-full opacity-0 group-hover:opacity-100 transition-opacity" />
                    <CardContent className="p-6 space-y-4">
                      <div className="flex items-start justify-between">
                        <div 
                          className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                          style={{ backgroundColor: `${category.color}15` }}
                        >
                          <span role="img" aria-label={category.label}>{category.icon}</span>
                        </div>
                        {identity.is_coming_soon && (
                          <span className="text-xs font-medium px-2 py-1 rounded bg-[var(--color-surface-hover)] text-[var(--color-text-muted)]">
                            Soon
                          </span>
                        )}
                      </div>
                      <div>
                        <h3 className="font-semibold text-[var(--color-text)] mb-1">
                          {identity.name}
                        </h3>
                        <p className="text-sm text-[var(--color-text-secondary)] line-clamp-2">
                          {identity.tagline}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
