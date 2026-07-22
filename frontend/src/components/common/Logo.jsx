"use client";

/**
 * SelfGPT — Logo Component
 *
 * SVG wordmark with optional icon-only mode.
 */
export function Logo({ size = "default", showText = true, className = "" }) {
  const sizes = {
    small: { icon: 24, text: "text-base" },
    default: { icon: 32, text: "text-xl" },
    large: { icon: 48, text: "text-3xl" },
    hero: { icon: 64, text: "text-hero" },
  };

  const s = sizes[size] || sizes.default;

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {/* Icon — stylized "S" with amber accent */}
      <svg
        width={s.icon}
        height={s.icon}
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <rect
          width="48"
          height="48"
          rx="12"
          fill="var(--color-accent)"
        />
        <path
          d="M32 16.5C32 16.5 29.5 13 24 13C18.5 13 15 16.5 15 19.5C15 22.5 17.5 24 24 25.5C30.5 27 33 28.5 33 31.5C33 34.5 29.5 37 24 37C18.5 37 16 33.5 16 33.5"
          stroke="white"
          strokeWidth="3.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      {showText && (
        <span
          className={`font-bold tracking-tight ${s.text}`}
          style={{ color: "var(--color-text)" }}
        >
          Self
          <span style={{ color: "var(--color-accent)" }}>GPT</span>
        </span>
      )}
    </div>
  );
}

export default Logo;
