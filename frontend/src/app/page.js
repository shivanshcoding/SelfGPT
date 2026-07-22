import { Hero } from "@/components/landing/Hero";
import { Identities } from "@/components/landing/Identities";
import { Roadmap } from "@/components/landing/Roadmap";
import { CTA } from "@/components/landing/CTA";

export default function LandingPage() {
  return (
    <main className="flex flex-col min-h-screen">
      {/* Header/Nav (simplified for landing) */}
      <header className="absolute top-0 left-0 right-0 z-50 py-6">
        <div className="container mx-auto px-6 flex justify-between items-center">
          <div className="w-32" /> {/* Spacer for centering if needed, or Logo */}
          <nav className="hidden md:flex items-center gap-8 font-medium text-[var(--color-text-secondary)]">
            <a href="#identities" className="hover:text-[var(--color-text)] transition-colors">Identities</a>
            <a href="/login" className="hover:text-[var(--color-text)] transition-colors">Sign In</a>
            <a 
              href="/register" 
              className="px-4 py-2 rounded-lg text-white text-sm"
              style={{ backgroundColor: "var(--color-accent)" }}
            >
              Sign Up
            </a>
          </nav>
        </div>
      </header>

      <Hero />
      <Identities />
      <Roadmap />
      <CTA />
      
      <footer className="py-8 border-t border-[var(--color-border)] text-center text-sm text-[var(--color-text-muted)]">
        <p>© {new Date().getFullYear()} SelfGPT. All rights reserved.</p>
      </footer>
    </main>
  );
}
