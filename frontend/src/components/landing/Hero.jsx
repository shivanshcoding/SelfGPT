"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import Logo from "@/components/common/Logo";

export function Hero() {
  return (
    <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[var(--color-accent)]/10 rounded-full blur-[100px] pointer-events-none" />

      <div className="container mx-auto px-6 relative z-10">
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto space-y-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, type: "spring", bounce: 0.4 }}
            className="flex justify-center"
          >
            <Logo size="hero" className="mb-4" />
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-display md:text-hero font-bold tracking-tight text-[var(--color-text)]"
          >
            Every conversation.<br className="hidden md:block" />
            <span className="text-[var(--color-text-secondary)]">
              A new perspective.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-heading md:text-2xl font-medium text-[var(--color-text-secondary)] max-w-2xl"
          >
            Converse with famous personalities, historical figures, fictional characters, 
            and your own custom AI — all powered by open-source LLMs.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 pt-8"
          >
            <Link
              href="/register"
              className="px-8 py-4 rounded-xl text-lg font-medium text-white shadow-lg transition-all hover:scale-105 active:scale-95"
              style={{
                backgroundColor: "var(--color-accent)",
                boxShadow: "var(--shadow-md)",
              }}
            >
              Get Started for Free
            </Link>
            <Link
              href="#identities"
              className="px-8 py-4 rounded-xl text-lg font-medium transition-all hover:bg-[var(--color-surface)] border border-[var(--color-border)]"
            >
              Explore Identities
            </Link>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
