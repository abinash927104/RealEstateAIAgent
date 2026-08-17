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
      content: "Hello! 👋 I'm your AI Real Estate Assistant. How can I help you today?",
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

  const handleSend = async (overrideInput?: string) => {
    const textToSend = overrideInput || input;
    const trimmed = textToSend.trim();
    if (!trimmed || loading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: trimmed,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    if (!overrideInput) setInput("");
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

  const quickActions = [
    {
      icon: "🏠",
      title: "Property Search",
      description: "Find homes matching your criteria",
      prompt: "Find 3 BHK apartments in Bangalore under ₹2 Crores on MagicBricks",
      gradient: "linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(14, 165, 233, 0.1) 100%)",
      border: "rgba(20, 184, 166, 0.3)",
      hoverBorder: "rgba(20, 184, 166, 0.8)",
    },
    {
      icon: "💰",
      title: "Mortgage Calculator",
      description: "Calculate monthly payments",
      prompt: "Calculate EMI for a ₹1.5 Cr home with ₹30L down payment at 8.5% interest over 20 years",
      gradient: "linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(217, 70, 239, 0.1) 100%)",
      border: "rgba(139, 92, 246, 0.3)",
      hoverBorder: "rgba(139, 92, 246, 0.8)",
    },
    {
      icon: "📈",
      title: "Investment Analysis",
      description: "Evaluate ROI on rental properties",
      prompt: "What is the ROI on a ₹80 Lakh rental yielding ₹35k/month?",
      gradient: "linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%)",
      border: "rgba(245, 158, 11, 0.3)",
      hoverBorder: "rgba(245, 158, 11, 0.8)",
    },
    {
      icon: "🏘️",
      title: "Market Analysis",
      description: "Get market trends and data",
      prompt: "What are the real estate market trends in Mumbai right now?",
      gradient: "linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)",
      border: "rgba(16, 185, 129, 0.3)",
      hoverBorder: "rgba(16, 185, 129, 0.8)",
    }
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
                      {msg.toolsUsed.map((tool, index) => (
                        <span
                          key={`${tool}-${index}`}
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

            {/* Quick Actions Grid (Shown only on new conversation) */}
            {messages.length <= 1 && (
              <div className="animate-fade-in" style={{ marginTop: 24, marginBottom: 32 }}>
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
                    gap: 16,
                  }}
                >
                  {quickActions.map((action, idx) => (
                    <div
                      key={idx}
                      onClick={() => handleSend(action.prompt)}
                      style={{
                        padding: 20,
                        borderRadius: 16,
                        background: action.gradient,
                        border: `1px solid ${action.border}`,
                        cursor: "pointer",
                        transition: "all 0.2s ease",
                        display: "flex",
                        flexDirection: "column",
                        gap: 8,
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = "translateY(-2px)";
                        e.currentTarget.style.borderColor = action.hoverBorder;
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = "translateY(0)";
                        e.currentTarget.style.borderColor = action.border;
                      }}
                    >
                      <div style={{ fontSize: "1.8rem" }}>{action.icon}</div>
                      <h4 style={{ margin: 0, fontSize: "1.05rem", fontWeight: 600, color: "var(--color-text-primary)" }}>
                        {action.title}
                      </h4>
                      <p style={{ margin: 0, fontSize: "0.85rem", color: "var(--color-text-secondary)", lineHeight: 1.4 }}>
                        {action.description}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

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
              onClick={() => handleSend()}
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
