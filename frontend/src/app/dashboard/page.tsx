"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import { analyticsApi, type DashboardAnalytics } from "@/lib/api";

export default function DashboardPage() {
  const [analytics, setAnalytics] = useState<DashboardAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const token = localStorage.getItem("access_token") || "";
        const data = await analyticsApi.getDashboard(token);
        setAnalytics(data);
      } catch {
        console.error("Failed to fetch dashboard data");
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  const statCards = [
    {
      icon: "🔍",
      label: "Total Searches",
      value: analytics?.total_searches ?? 0,
      gradient: "linear-gradient(135deg, #14b8a6, #0ea5e9)",
    },
    {
      icon: "💬",
      label: "Conversations",
      value: analytics?.total_conversations ?? 0,
      gradient: "linear-gradient(135deg, #8b5cf6, #ec4899)",
    },
    {
      icon: "❤️",
      label: "Saved Properties",
      value: analytics?.total_favorites ?? 0,
      gradient: "linear-gradient(135deg, #ef4444, #f59e0b)",
    },
    {
      icon: "⚡",
      label: "Avg Response",
      value: `${(analytics?.avg_response_time_ms ?? 0).toFixed(0)}ms`,
      gradient: "linear-gradient(135deg, #22c55e, #14b8a6)",
    },
  ];

  return (
    <>
      <Navbar />
      <div style={{ paddingTop: 64, minHeight: "100vh", background: "var(--color-surface)" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "48px 24px" }}>
          {/* Header */}
          <div style={{ marginBottom: 40 }}>
            <h1
              style={{
                fontSize: "clamp(1.8rem, 4vw, 2.5rem)",
                fontWeight: 800,
                fontFamily: "var(--font-heading)",
                marginBottom: 8,
              }}
            >
              Your <span className="gradient-text">Dashboard</span>
            </h1>
            <p style={{ color: "var(--color-text-secondary)", fontSize: "1.05rem" }}>
              Track your real estate journey
            </p>
          </div>

          {/* Stats Grid */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: 20,
              marginBottom: 40,
            }}
            className="stagger-children"
          >
            {statCards.map((stat) => (
              <div
                key={stat.label}
                className="glass-card"
                style={{
                  padding: 24,
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                }}
              >
                <div
                  style={{
                    width: 50,
                    height: 50,
                    borderRadius: 14,
                    background: stat.gradient,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 24,
                    flexShrink: 0,
                  }}
                >
                  {stat.icon}
                </div>
                <div>
                  <div
                    style={{
                      fontSize: "1.5rem",
                      fontWeight: 800,
                      fontFamily: "var(--font-heading)",
                      color: "var(--color-text-primary)",
                    }}
                  >
                    {loading ? "..." : stat.value}
                  </div>
                  <div
                    style={{
                      fontSize: "0.8rem",
                      color: "var(--color-text-muted)",
                      marginTop: 2,
                    }}
                  >
                    {stat.label}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Quick Actions */}
          <div style={{ marginBottom: 40 }}>
            <h2
              style={{
                fontSize: "1.3rem",
                fontWeight: 700,
                fontFamily: "var(--font-heading)",
                marginBottom: 16,
              }}
            >
              Quick Actions
            </h2>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                gap: 16,
              }}
            >
              {[
                { icon: "💬", label: "New Chat", href: "/chat", desc: "Start a conversation" },
                { icon: "🏠", label: "Browse Properties", href: "/properties", desc: "Explore listings" },
                { icon: "💰", label: "Calculate Mortgage", href: "/chat", desc: "Ask in chat" },
                { icon: "📈", label: "Analyze ROI", href: "/chat", desc: "Investment analysis" },
              ].map((action) => (
                <a
                  key={action.label}
                  href={action.href}
                  className="glass-card"
                  style={{
                    padding: 20,
                    textDecoration: "none",
                    color: "inherit",
                    textAlign: "center",
                  }}
                >
                  <div style={{ fontSize: "2rem", marginBottom: 8 }}>{action.icon}</div>
                  <div style={{ fontWeight: 600, fontSize: "0.95rem", marginBottom: 4 }}>
                    {action.label}
                  </div>
                  <div style={{ fontSize: "0.8rem", color: "var(--color-text-muted)" }}>
                    {action.desc}
                  </div>
                </a>
              ))}
            </div>
          </div>

          {/* Info box */}
          <div
            className="glass-card"
            style={{
              padding: 32,
              textAlign: "center",
              borderColor: "var(--color-border-accent)",
            }}
          >
            <div style={{ fontSize: "2rem", marginBottom: 12 }}>🤖</div>
            <h3
              style={{
                fontSize: "1.2rem",
                fontWeight: 700,
                marginBottom: 8,
                fontFamily: "var(--font-heading)",
              }}
            >
              Your AI Assistant is Ready
            </h3>
            <p
              style={{
                color: "var(--color-text-secondary)",
                fontSize: "0.95rem",
                maxWidth: 500,
                margin: "0 auto 20px",
              }}
            >
              Start chatting to search properties, calculate mortgages, analyze investments,
              and get market insights — all in natural language.
            </p>
            <a href="/chat" className="btn-primary" style={{ padding: "12px 28px" }}>
              🚀 Start Chatting
            </a>
          </div>
        </div>
      </div>
    </>
  );
}
