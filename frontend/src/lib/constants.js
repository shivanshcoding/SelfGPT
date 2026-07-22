/**
 * SelfGPT — Constants
 */

export const APP_NAME = "SelfGPT";
export const APP_TAGLINE = "Every conversation. A new perspective.";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const WS_BASE_URL =
  process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export const IDENTITY_CATEGORIES = {
  famous_personality: {
    label: "Famous Personalities",
    icon: "🌟",
    color: "#F5A623",
    description: "Converse with AI simulations inspired by the world's most influential minds",
  },
  famous_book: {
    label: "Famous Books",
    icon: "📚",
    color: "#007AFF",
    description: "Chat with the spirit of legendary books — wisdom distilled into conversation",
  },
  fictional_character: {
    label: "Fictional Characters",
    icon: "🎭",
    color: "#AF52DE",
    description: "Step into conversations with the most iconic characters from fiction",
  },
  historical_figure: {
    label: "Historical Figures",
    icon: "🏛️",
    color: "#8B6914",
    description: "Learn from the greatest minds in human history",
  },
  cartoon_character: {
    label: "Cartoon Characters",
    icon: "🎨",
    color: "#FF3B30",
    description: "Bring your favorite animated characters to life through AI conversation",
  },
  custom: {
    label: "Custom Identity",
    icon: "✨",
    color: "#34C759",
    description: "Build your own AI personality from scratch",
  },
};

export const COMING_SOON_MODULES = [
  {
    name: "Life Planner",
    description: "Long-term goals to daily plans — your AI life strategist",
    icon: "🗺️",
  },
  {
    name: "Dilemma Solver",
    description: "Navigate tough decisions with structured AI reasoning",
    icon: "⚖️",
  },
  {
    name: "Daily Coach",
    description: "Your personal AI coach for daily growth and accountability",
    icon: "💪",
  },
  {
    name: "Goal Tracker",
    description: "Set, track, and achieve your goals with AI guidance",
    icon: "🎯",
  },
  {
    name: "Habit Builder",
    description: "Build lasting habits with AI-powered nudges and tracking",
    icon: "🔄",
  },
  {
    name: "Calendar & Tasks",
    description: "Smart task management integrated with your calendar",
    icon: "📅",
  },
];

export const PERSONALITY_TRAITS = [
  { key: "humor", label: "Humor", min: "Serious", max: "Witty" },
  { key: "empathy", label: "Empathy", min: "Objective", max: "Empathetic" },
  { key: "strictness", label: "Strictness", min: "Flexible", max: "Strict" },
  { key: "creativity", label: "Creativity", min: "Practical", max: "Creative" },
  { key: "confidence", label: "Confidence", min: "Humble", max: "Bold" },
];
