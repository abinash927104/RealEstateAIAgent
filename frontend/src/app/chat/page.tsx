"use client";

import { useState, useRef, useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import { chatApi, type ChatMessage } from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  toolsUsed?: string[];
  queryType?: string;
  timestamp: Date;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hello! 👋 I'm your AI Real Estate Assistant. I can help you with:\n\n🏠 **Property Search** — Find homes matching your criteria\n💰 **Mortgage Calculator** — Calculate monthly payments\n📈 **Investment Analysis** — Evaluate ROI on rental properties\n🏘️ **Market Analysis** — Get market trends and data\n\nWhat would you like to explore?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: trimmed,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const token = localStorage.getItem("access_token") || "";
      const response = await chatApi.sendMessage(trimmed, conversationId, token);

      if (response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      const assistantMessage: Message = {
        id: response.message.id,
        role: "assistant",
        content: response.message.content,
        toolsUsed: response.tools_used,
        queryType: response.query_type || undefined,
        timestamp: new Date(response.message.created_at),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      const isAuthError = error?.status === 401;
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content: isAuthError 
          ? "🔒 **Authentication Required**\nPlease log in or register an account to chat with the AI assistant."
          : "Sorry, I encountered an error while communicating with the server. Please check your connection and try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const renderContent = (text: string) => {
    // Basic markdown-like rendering
    return text.split("\n").map((line, i) => {
      // Bold
      const processed = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      // Headers
      if (line.startsWith("# ")) {
        return <h3 key={i} style={{ fontSize: "1.1rem", fontWeight: 700, margin: "8px 0" }} dangerouslySetInnerHTML={{ __html: processed.slice(2) }} />;
      }
      // Tables
      if (line.startsWith("|")) {
        return (
          <div key={i} style={{ fontFamily: "monospace", fontSize: "0.85rem", color: "var(--color-text-secondary)" }} dangerouslySetInnerHTML={{ __html: processed }} />
        );
      }
      // Empty lines
      if (line.trim() === "") return <br key={i} />;
      // Normal text
      return <p key={i} style={{ margin: "2px 0", lineHeight: 1.6 }} dangerouslySetInnerHTML={{ __html: processed }} />;
    });
  };

  const quickPrompts = [
    "Find 3-bed homes in Austin under $500K",
    "Calculate mortgage for a $400K home",
    "What's the ROI on a $300K rental at $2K/month rent?",
    "Market analysis for Miami, FL",
  ];

  return (
    <>
      <Navbar />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100vh",
          paddingTop: 64,
          background: "var(--color-surface)",
        }}
      >
        {/* Messages area */}
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            padding: "24px 16px",
          }}
        >
          <div style={{ maxWidth: 800, margin: "0 auto" }}>
            {messages.map((msg) => (
              <div
                key={msg.id}
                className="animate-fade-in"
                style={{
                  display: "flex",
                  justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
                  marginBottom: 16,
                }}
              >
                <div
                  style={{
                    maxWidth: "85%",
                    padding: "14px 18px",
                    borderRadius: msg.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                    background:
                      msg.role === "user"
                        ? "linear-gradient(135deg, #14b8a6 0%, #0ea5e9 100%)"
                        : "var(--color-surface-elevated)",
                    border: msg.role === "user" ? "none" : "1px solid var(--color-border)",
                    color: "var(--color-text-primary)",
                    fontSize: "0.92rem",
                    lineHeight: 1.6,
                    wordBreak: "break-word",
                  }}
                >
                  {renderContent(msg.content)}

                  {/* Tools used badge */}
                  {msg.toolsUsed && msg.toolsUsed.length > 0 && (
                    <div
                      style={{
                        marginTop: 10,
                        display: "flex",
                        gap: 6,
                        flexWrap: "wrap",
                      }}
                    >
                      {msg.toolsUsed.map((tool) => (
                        <span
                          key={tool}
                          style={{
                            fontSize: "0.7rem",
                            padding: "3px 8px",
                            borderRadius: 9999,
                            background: "rgba(20, 184, 166, 0.15)",
                            color: "var(--color-accent)",
                            fontWeight: 500,
                          }}
                        >
                          🔧 {tool.replace(/_/g, " ")}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* Typing indicator */}
            {loading && (
              <div style={{ display: "flex", justifyContent: "flex-start", marginBottom: 16 }}>
                <div
                  style={{
                    padding: "14px 18px",
                    borderRadius: "18px 18px 18px 4px",
                    background: "var(--color-surface-elevated)",
                    border: "1px solid var(--color-border)",
                  }}
                >
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Quick prompts */}
        {messages.length <= 1 && (
          <div
            style={{
              padding: "0 16px 12px",
              display: "flex",
              gap: 8,
              justifyContent: "center",
              flexWrap: "wrap",
              maxWidth: 800,
              margin: "0 auto",
              width: "100%",
            }}
          >
            {quickPrompts.map((prompt) => (
              <button
                key={prompt}
                onClick={() => {
                  setInput(prompt);
                  setTimeout(() => inputRef.current?.focus(), 50);
                }}
                style={{
                  padding: "8px 14px",
                  borderRadius: 9999,
                  border: "1px solid var(--color-border)",
                  background: "var(--color-surface-elevated)",
                  color: "var(--color-text-secondary)",
                  fontSize: "0.8rem",
                  cursor: "pointer",
                  transition: "all 0.2s",
                  whiteSpace: "nowrap",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = "var(--color-accent)";
                  e.currentTarget.style.color = "var(--color-accent)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = "var(--color-border)";
                  e.currentTarget.style.color = "var(--color-text-secondary)";
                }}
              >
                {prompt}
              </button>
            ))}
          </div>
        )}

        {/* Input area */}
        <div
          style={{
            borderTop: "1px solid var(--color-border)",
            padding: "16px",
            background: "rgba(15, 23, 42, 0.95)",
            backdropFilter: "blur(16px)",
          }}
        >
          <div
            style={{
              maxWidth: 800,
              margin: "0 auto",
              display: "flex",
              gap: 12,
              alignItems: "flex-end",
            }}
          >
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me about properties, mortgages, investments..."
              rows={1}
              style={{
                flex: 1,
                padding: "12px 16px",
                borderRadius: 16,
                border: "1px solid var(--color-border)",
                background: "var(--color-surface-elevated)",
                color: "var(--color-text-primary)",
                fontSize: "0.95rem",
                fontFamily: "var(--font-body)",
                resize: "none",
                outline: "none",
                maxHeight: 120,
                transition: "border-color 0.2s",
              }}
              onFocus={(e) => (e.target.style.borderColor = "var(--color-accent)")}
              onBlur={(e) => (e.target.style.borderColor = "var(--color-border)")}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="btn-primary"
              style={{
                padding: "12px 20px",
                borderRadius: 16,
                fontSize: "1.1rem",
                opacity: !input.trim() || loading ? 0.5 : 1,
                cursor: !input.trim() || loading ? "not-allowed" : "pointer",
                minWidth: 52,
              }}
            >
              ➤
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
