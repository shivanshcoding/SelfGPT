"use client";

import { memo } from "react";
import { motion } from "framer-motion";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn, formatDate } from "@/lib/utils";
import ReactMarkdown from "react-markdown";
import { Bot, User } from "lucide-react";

export const MessageBubble = memo(({ message, isStreaming = false }) => {
  const isUser = message.role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "group flex w-full max-w-4xl mx-auto gap-4 py-6 px-4 md:px-0",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      {/* Avatar */}
      <div className="flex-shrink-0 flex flex-col items-center">
        <Avatar className="w-8 h-8 md:w-10 md:h-10 border border-[var(--color-border)] shadow-sm">
          {isUser ? (
            <>
              <AvatarFallback className="bg-[var(--color-accent)] text-white font-semibold">
                U
              </AvatarFallback>
            </>
          ) : (
            <>
              <AvatarImage src={`/identities/${message.identity_id}.png`} />
              <AvatarFallback className="bg-[var(--color-surface-active)] text-[var(--color-text)]">
                <Bot size={18} />
              </AvatarFallback>
            </>
          )}
        </Avatar>
      </div>

      {/* Bubble */}
      <div
        className={cn(
          "flex flex-col max-w-[85%] md:max-w-[75%]",
          isUser ? "items-end" : "items-start"
        )}
      >
        <div className="flex items-baseline gap-2 mb-1 px-1">
          <span className="text-sm font-medium text-[var(--color-text)]">
            {isUser ? "You" : message.identity_name || "SelfGPT"}
          </span>
          {message.created_at && (
            <span className="text-xs text-[var(--color-text-muted)]">
              {formatDate(message.created_at)}
            </span>
          )}
        </div>

        <div
          className={cn(
            "relative px-4 py-3 rounded-2xl text-[15px] leading-relaxed shadow-sm",
            isUser
              ? "bg-[var(--color-bubble-user)] text-[var(--color-bubble-user-text)] rounded-tr-sm"
              : "bg-[var(--color-bubble-ai)] text-[var(--color-bubble-ai-text)] rounded-tl-sm border border-[var(--color-border)]"
          )}
        >
          {/* Markdown Content */}
          <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none break-words">
            {isUser ? (
              <p className="whitespace-pre-wrap m-0">{message.content}</p>
            ) : (
              <ReactMarkdown>{message.content}</ReactMarkdown>
            )}
          </div>

          {/* Streaming Cursor */}
          {isStreaming && (
            <span className="inline-block w-2 h-4 ml-1 align-middle bg-[var(--color-text)] animate-pulse" />
          )}
        </div>

        {/* Action bar (copy, regenerate, thumbs up/down) - visible on hover */}
        {!isUser && !isStreaming && (
          <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
            {/* Action buttons will go here (Coming Soon) */}
            <span className="text-xs text-[var(--color-text-muted)]">
              {message.model_id}
            </span>
          </div>
        )}
      </div>
    </motion.div>
  );
});

MessageBubble.displayName = "MessageBubble";
