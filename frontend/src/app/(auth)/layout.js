import Logo from "@/components/common/Logo";

export default function AuthLayout({ children }) {
  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-[var(--color-bg)]">
      {/* Left side: branding/imagery */}
      <div className="hidden md:flex flex-1 flex-col items-center justify-center p-8 bg-[var(--color-surface)] border-r border-[var(--color-border)]">
        <div className="max-w-md text-center space-y-6">
          <Logo size="hero" className="justify-center mb-8" />
          <h1 className="text-display font-semibold text-[var(--color-text)]">
            Every conversation.<br />
            A new perspective.
          </h1>
          <p className="text-body text-[var(--color-text-secondary)]">
            Explore diverse AI identities powered by state-of-the-art 
            open source models, directly from your device.
          </p>
        </div>
      </div>

      {/* Right side: auth forms */}
      <div className="flex-1 flex flex-col items-center justify-center p-6 md:p-12 relative">
        <div className="absolute top-8 left-8 md:hidden">
          <Logo size="default" />
        </div>
        <div className="w-full max-w-[400px]">
          {children}
        </div>
      </div>
    </div>
  );
}
