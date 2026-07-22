"use client";

import { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import useAuthStore from "@/stores/authStore";
import { MessageBubble } from "@/components/chat/MessageBubble";
import { ChatInput } from "@/components/chat/ChatInput";
import { toast } from "sonner";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ArrowDown } from "lucide-react";

export default function ChatPage() {
  const params = useParams();
  const chatId = params?.chatId;
  const router = useRouter();
  const token = useAuthStore(s => s.accessToken);
  
  const [messages, setMessages] = useState([]);
  const [chat, setChat] = useState(null);
  const [identity, setIdentity] = useState(null);
  
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const wsRef = useRef(null);
  const scrollRef = useRef(null);
  
  const [showScrollBottom, setShowScrollBottom] = useState(false);

  useEffect(() => {
    if (chatId) {
      fetchChatData();
    }
  }, [chatId]);

  const fetchChatData = async () => {
    try {
      const [chatRes, msgsRes, idRes] = await Promise.all([
        api.get(`/api/chats/${chatId}`),
        api.get(`/api/chats/${chatId}/messages/`),
        api.get("/api/identities/")
      ]);
      setChat(chatRes.data);
      setMessages(msgsRes.data);
      
      const identityObj = idRes.data.identities.find(i => i.slug === chatRes.data.identity_id);
      setIdentity(identityObj);
    } catch (err) {
      toast.error("Failed to load chat.");
      router.push("/chat");
    }
  };

  const scrollToBottom = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    // Auto-scroll when messages change or while streaming
    scrollToBottom();
  }, [messages, streamingContent]);

  const handleScroll = (e) => {
    const target = e.target;
    // Show scroll button if we are scrolled up more than 100px from bottom
    const isScrolledUp = target.scrollHeight - target.scrollTop - target.clientHeight > 100;
    setShowScrollBottom(isScrolledUp);
  };

  const handleSendMessage = async (content) => {
    if (!content.trim()) return;
    
    // Optimistically add user message
    const tempId = `temp_${Date.now()}`;
    const userMsg = {
      id: tempId,
      role: "user",
      content: content,
      created_at: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMsg]);
    setIsStreaming(true);
    setStreamingContent("");

    // Initialize WebSocket
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";
    const ws = new WebSocket(`${wsUrl}/api/ws/chat/${chatId}/stream?token=${token}`);
    wsRef.current = ws;

    ws.onopen = () => {
      ws.send(JSON.stringify({ content }));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === "token") {
        setStreamingContent(prev => prev + data.content);
      } else if (data.type === "done") {
        // Stream complete, fetch fresh messages to get actual IDs
        setIsStreaming(false);
        ws.close();
        fetchChatData(); 
      } else if (data.type === "error") {
        toast.error(data.content || "Error generating response");
        setIsStreaming(false);
        ws.close();
      }
    };

    ws.onerror = () => {
      toast.error("WebSocket connection error");
      setIsStreaming(false);
    };

    ws.onclose = () => {
      setIsStreaming(false);
    };
  };

  const handleStop = () => {
    if (wsRef.current) {
      wsRef.current.close();
      setIsStreaming(false);
      // We don't have partial saving implemented on backend on disconnect yet, 
      // but in a prod scenario the backend would save what it generated so far.
      fetchChatData();
    }
  };

  return (
    <div className="flex flex-col h-full bg-[var(--color-bg)] relative">
      
      {/* Chat Header */}
      <header className="flex-shrink-0 p-4 border-b border-[var(--color-border)] flex items-center justify-between bg-[var(--color-bg)]/80 backdrop-blur-md z-10 sticky top-0">
        <div className="flex items-center gap-3 md:ml-12"> {/* ML to account for floating sidebar toggle on mobile */}
          <h2 className="font-semibold text-[var(--color-text)]">
            {identity?.name || chat?.title || "Loading..."}
          </h2>
          {identity?.is_coming_soon && (
             <span className="text-xs px-2 py-0.5 rounded bg-[var(--color-accent-soft)] text-[var(--color-accent-hover)] font-medium">
               Alpha
             </span>
          )}
        </div>
      </header>

      {/* Messages Area */}
      <ScrollArea className="flex-1" onScrollCapture={handleScroll}>
        <div className="pb-8 pt-4">
          {messages.length === 0 && !isStreaming ? (
            <div className="h-full flex items-center justify-center mt-32">
              <div className="text-center space-y-4">
                <div className="w-16 h-16 rounded-2xl bg-[var(--color-surface)] flex items-center justify-center mx-auto text-3xl">
                  👋
                </div>
                <h3 className="text-xl font-medium text-[var(--color-text)]">
                  Start a conversation
                </h3>
                <p className="text-sm text-[var(--color-text-muted)]">
                  Message {identity?.name} to get started
                </p>
              </div>
            </div>
          ) : (
            <>
              {messages.map(msg => (
                <MessageBubble key={msg.id} message={{...msg, identity_name: identity?.name}} />
              ))}
              
              {isStreaming && (
                <MessageBubble 
                  message={{ 
                    role: "assistant", 
                    content: streamingContent, 
                    identity_id: identity?.slug,
                    identity_name: identity?.name
                  }} 
                  isStreaming={true} 
                />
              )}
            </>
          )}
          {/* Invisible div for auto-scrolling */}
          <div ref={scrollRef} className="h-4" />
        </div>
      </ScrollArea>

      {/* Scroll to bottom button */}
      {showScrollBottom && (
        <button
          onClick={scrollToBottom}
          className="absolute bottom-24 right-1/2 translate-x-1/2 p-2 rounded-full bg-[var(--color-surface)] border border-[var(--color-border)] shadow-md text-[var(--color-text-secondary)] hover:text-[var(--color-text)] z-20 transition-all"
        >
          <ArrowDown size={18} />
        </button>
      )}

      {/* Input Area */}
      <div className="flex-shrink-0 bg-gradient-to-t from-[var(--color-bg)] via-[var(--color-bg)] to-transparent pt-6 relative z-10">
        <ChatInput 
          onSendMessage={handleSendMessage} 
          isStreaming={isStreaming} 
          onStop={handleStop}
        />
      </div>
    </div>
  );
}
