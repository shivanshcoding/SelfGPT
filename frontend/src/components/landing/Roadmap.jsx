"use client";

import { motion } from "framer-motion";
import { COMING_SOON_MODULES } from "@/lib/constants";
import { Card, CardContent } from "@/components/ui/card";

export function Roadmap() {
  return (
    <section className="py-24 bg-[var(--color-bg)] border-y border-[var(--color-border)]">
      <div className="container mx-auto px-6">
        <div className="flex flex-col lg:flex-row items-center gap-16 max-w-6xl mx-auto">
          {/* Left side text */}
          <div className="flex-1 space-y-8">
            <div className="inline-block px-4 py-1.5 rounded-full text-sm font-semibold bg-[var(--color-accent-soft)] text-[var(--color-accent-hover)]">
              Coming Soon
            </div>
            <h2 className="text-display font-bold text-[var(--color-text)] leading-tight">
              More than just chat. <br />
              <span className="text-[var(--color-text-muted)]">Your intelligent operating system.</span>
            </h2>
            <p className="text-heading text-[var(--color-text-secondary)]">
              We're building specialized modules to help you navigate life's complexities. 
              From setting goals to solving dilemmas, your AI identities will soon act as 
              dedicated tools.
            </p>
          </div>

          {/* Right side grid */}
          <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
            {COMING_SOON_MODULES.map((module, index) => (
              <motion.div
                key={module.name}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
              >
                <Card className="h-full bg-[var(--color-surface)] border-transparent">
                  <CardContent className="p-6">
                    <div className="text-2xl mb-3">{module.icon}</div>
                    <h3 className="font-semibold text-[var(--color-text)] mb-1">
                      {module.name}
                    </h3>
                    <p className="text-sm text-[var(--color-text-secondary)]">
                      {module.description}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
