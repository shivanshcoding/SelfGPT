"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export function CTA() {
  return (
    <section className="py-24 bg-[var(--color-bg)]">
      <div className="container mx-auto px-6">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto rounded-3xl p-12 text-center relative overflow-hidden"
          style={{ backgroundColor: "var(--color-surface)" }}
        >
          {/* Decorative circles */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-[var(--color-accent)]/10 rounded-full blur-[80px]" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/10 rounded-full blur-[80px]" />

          <div className="relative z-10 space-y-8">
            <h2 className="text-display font-bold text-[var(--color-text)]">
              Ready to start the conversation?
            </h2>
            <p className="text-heading text-[var(--color-text-secondary)] max-w-2xl mx-auto">
              Join SelfGPT today and connect with AI identities that offer fresh 
              perspectives on your daily life.
            </p>
            <div className="pt-4">
              <Link
                href="/register"
                className="inline-block px-10 py-5 rounded-xl text-lg font-bold text-white shadow-lg transition-transform hover:scale-105 active:scale-95"
                style={{ backgroundColor: "var(--color-accent)" }}
              >
                Create your free account
              </Link>
            </div>
            <p className="text-sm text-[var(--color-text-muted)] mt-6">
              100% Free · Open Source Models · Privacy First
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
