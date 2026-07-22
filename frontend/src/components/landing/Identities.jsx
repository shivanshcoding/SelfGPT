"use client";

import { motion } from "framer-motion";
import { IDENTITY_CATEGORIES } from "@/lib/constants";
import { Card, CardContent } from "@/components/ui/card";

export function Identities() {
  const categories = Object.values(IDENTITY_CATEGORIES);

  return (
    <section id="identities" className="py-24 bg-[var(--color-surface)]">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-display font-bold text-[var(--color-text)]">
            Who will you talk to today?
          </h2>
          <p className="text-heading text-[var(--color-text-secondary)] max-w-2xl mx-auto">
            Choose from five distinct categories, or build your own custom identity from scratch.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {categories.map((cat, index) => (
            <motion.div
              key={cat.label}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="h-full border-transparent hover:border-[var(--color-accent)]/30 hover:shadow-lg transition-all duration-300 bg-[var(--color-bg)]">
                <CardContent className="p-8 space-y-6">
                  <div
                    className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl"
                    style={{ backgroundColor: `${cat.color}15` }}
                  >
                    <span role="img" aria-label={cat.label}>{cat.icon}</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2 text-[var(--color-text)]">
                      {cat.label}
                    </h3>
                    <p className="text-[var(--color-text-secondary)] leading-relaxed">
                      {cat.description}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
