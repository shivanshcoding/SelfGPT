import { Toaster } from "sonner";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { ThemeInitializer } from "@/components/common/ThemeInitializer";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains",
  subsets: ["latin"],
  display: "swap",
});

export const metadata = {
  title: "SelfGPT — Every conversation. A new perspective.",
  description:
    "Talk to different AI identities — famous personalities, legendary books, " +
    "fictional characters, historical figures, and your own custom persona. " +
    "Powered by open-source multimodal LLMs.",
  keywords: [
    "AI chat", "AI identity", "custom AI", "personality AI",
    "open source LLM", "SelfGPT",
  ],
  authors: [{ name: "Shivansh Rana" }],
  openGraph: {
    title: "SelfGPT — Every conversation. A new perspective.",
    description:
      "Talk to different AI identities powered by open-source multimodal LLMs.",
    type: "website",
    siteName: "SelfGPT",
  },
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${inter.variable} ${jetbrainsMono.variable}`}
    >
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="min-h-screen bg-[var(--color-bg)] text-[var(--color-text)] font-[var(--font-inter)] antialiased transition-colors duration-200">
        <ThemeInitializer />
        {children}
        <Toaster position="top-center" richColors />
      </body>
    </html>
  );
}
