"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Image as ImageIcon, StopCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export function ChatInput({ onSendMessage, isStreaming, onStop }) {
  const [content, setContent] = useState("");
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [content]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSend = () => {
    if (content.trim() && !isStreaming) {
      onSendMessage(content.trim());
      setContent("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  return (
    <div className="relative max-w-4xl mx-auto w-full px-4 pb-4 md:pb-8">
      <div className="relative flex items-end w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl shadow-sm overflow-hidden transition-all focus-within:border-[var(--color-accent)] focus-within:ring-1 focus-within:ring-[var(--color-accent)]">
        
        {/* Attachment Button (Coming Soon) */}
        <button
          type="button"
          className="p-3 mb-1 ml-1 text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors rounded-xl"
          title="Attach image (Coming Soon)"
        >
          <ImageIcon size={20} />
        </button>

        {/* Textarea */}
        <textarea
          ref={textareaRef}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message SelfGPT..."
          className="flex-1 max-h-[200px] min-h-[44px] py-3 px-2 bg-transparent border-none resize-none focus:outline-none focus:ring-0 text-[var(--color-text)] text-body"
          rows={1}
        />

        {/* Send / Stop Button */}
        <div className="p-2 mb-1 mr-1">
          {isStreaming ? (
            <button
              onClick={onStop}
              className="p-2 bg-[var(--color-error)] text-white rounded-xl hover:opacity-90 transition-opacity flex items-center justify-center"
              title="Stop generating"
            >
              <StopCircle size={18} fill="currentColor" />
            </button>
          ) : (
            <button
              onClick={handleSend}
              disabled={!content.trim()}
              className={cn(
                "p-2 rounded-xl transition-all flex items-center justify-center",
                content.trim() 
                  ? "bg-[var(--color-accent)] text-white hover:bg-[var(--color-accent-hover)] shadow-sm"
                  : "bg-[var(--color-surface-hover)] text-[var(--color-text-muted)] cursor-not-allowed"
              )}
              title="Send message"
            >
              <Send size={18} />
            </button>
          )}
        </div>
      </div>
      
      <div className="text-center mt-2">
        <span className="text-caption text-[var(--color-text-muted)]">
          SelfGPT can make mistakes. Consider verifying important information.
        </span>
      </div>
    </div>
  );
}
