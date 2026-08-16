"use client";

import Navbar from "@/components/layout/Navbar";

const features = [
  {
    icon: "🏠",
    title: "Smart Property Search",
    description: "Find your perfect home with AI-powered natural language search. Just describe what you want.",
    gradient: "linear-gradient(135deg, #14b8a6, #0ea5e9)",
  },
  {
    icon: "💰",
    title: "Mortgage Calculator",
    description: "Get instant, accurate mortgage breakdowns including taxes, insurance, and HOA fees.",
    gradient: "linear-gradient(135deg, #f59e0b, #ef4444)",
  },
  {
    icon: "📈",
    title: "ROI Analysis",
    description: "Evaluate investment properties with cap rate, cash-on-cash return, and 5-year projections.",
    gradient: "linear-gradient(135deg, #8b5cf6, #ec4899)",
  },
  {
    icon: "🏘️",
    title: "Market Insights",
    description: "Access real-time market data, price trends, and neighborhood analytics.",
    gradient: "linear-gradient(135deg, #22c55e, #14b8a6)",
  },
];

const stats = [
  { value: "10K+", label: "Properties" },
  { value: "50+", label: "Cities" },
  { value: "99.9%", label: "Accuracy" },
  { value: "24/7", label: "AI Available" },
];

export default function HomePage() {
  return (
    <>
      <Navbar />

      {/* Hero Section */}
      <section
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "120px 1.5rem 80px",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Background glow effects */}
        <div
          style={{
            position: "absolute",
            top: "20%",
            left: "10%",
            width: 500,
            height: 500,
            background: "radial-gradient(circle, rgba(20, 184, 166, 0.08) 0%, transparent 70%)",
            borderRadius: "50%",
            filter: "blur(80px)",
            pointerEvents: "none",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: "10%",
            right: "10%",
            width: 400,
            height: 400,
            background: "radial-gradient(circle, rgba(14, 165, 233, 0.06) 0%, transparent 70%)",
            borderRadius: "50%",
            filter: "blur(80px)",
            pointerEvents: "none",
          }}
        />

        <div
          style={{
            maxWidth: 900,
            textAlign: "center",
            position: "relative",
            zIndex: 1,
          }}
          className="animate-slide-up"
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              padding: "6px 16px",
              borderRadius: 9999,
              border: "1px solid var(--color-border-accent)",
              background: "rgba(20, 184, 166, 0.08)",
              fontSize: "0.8rem",
              fontWeight: 500,
              color: "var(--color-accent)",
              marginBottom: 24,
            }}
          >
            ✨ Powered by GPT-4o AI
          </div>

          <h1
            style={{
              fontSize: "clamp(2.5rem, 6vw, 4.5rem)",
              fontWeight: 800,
              lineHeight: 1.1,
              marginBottom: 24,
              fontFamily: "var(--font-heading)",
            }}
          >
            Find Your Dream Home{" "}
            <span className="gradient-text">with AI</span>
          </h1>

          <p
            style={{
              fontSize: "clamp(1.05rem, 2vw, 1.25rem)",
              color: "var(--color-text-secondary)",
              maxWidth: 650,
              margin: "0 auto 40px",
              lineHeight: 1.7,
            }}
          >
            Search properties, calculate mortgages, analyze investments, and get
            market insights — all through natural conversation with our AI
            assistant.
          </p>

          <div style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
            <a href="/chat" className="btn-primary" style={{ padding: "14px 32px", fontSize: "1rem" }}>
              🚀 Start Chatting
            </a>
            <a href="/properties" className="btn-secondary" style={{ padding: "14px 32px", fontSize: "1rem" }}>
              Browse Properties
            </a>
          </div>

          {/* Stats */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: 24,
              marginTop: 80,
              maxWidth: 600,
              margin: "80px auto 0",
            }}
          >
            {stats.map((stat) => (
              <div key={stat.label} style={{ textAlign: "center" }}>
                <div
                  className="gradient-text"
                  style={{ fontSize: "2rem", fontWeight: 800, fontFamily: "var(--font-heading)" }}
                >
                  {stat.value}
                </div>
                <div style={{ fontSize: "0.85rem", color: "var(--color-text-muted)", marginTop: 4 }}>
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section
        style={{
          padding: "80px 1.5rem",
          maxWidth: 1200,
          margin: "0 auto",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: 60 }}>
          <h2
            style={{
              fontSize: "clamp(1.8rem, 4vw, 2.5rem)",
              fontWeight: 800,
              marginBottom: 16,
              fontFamily: "var(--font-heading)",
            }}
          >
            Everything You Need, <span className="gradient-text">One Conversation</span>
          </h2>
          <p style={{ color: "var(--color-text-secondary)", fontSize: "1.1rem", maxWidth: 550, margin: "0 auto" }}>
            Our AI agent combines multiple tools to give you comprehensive real estate guidance.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
            gap: 24,
          }}
          className="stagger-children"
        >
          {features.map((feature) => (
            <div
              key={feature.title}
              className="glass-card"
              style={{ padding: 32, cursor: "default" }}
            >
              <div
                style={{
                  width: 56,
                  height: 56,
                  borderRadius: 14,
                  background: feature.gradient,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 28,
                  marginBottom: 20,
                  boxShadow: "0 4px 16px rgba(0,0,0,0.3)",
                }}
              >
                {feature.icon}
              </div>
              <h3
                style={{
                  fontSize: "1.15rem",
                  fontWeight: 700,
                  marginBottom: 10,
                  fontFamily: "var(--font-heading)",
                }}
              >
                {feature.title}
              </h3>
              <p style={{ color: "var(--color-text-secondary)", fontSize: "0.92rem", lineHeight: 1.6 }}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section
        style={{
          padding: "80px 1.5rem",
          background: "var(--color-surface-elevated)",
        }}
      >
        <div style={{ maxWidth: 900, margin: "0 auto", textAlign: "center" }}>
          <h2
            style={{
              fontSize: "clamp(1.8rem, 4vw, 2.5rem)",
              fontWeight: 800,
              marginBottom: 16,
              fontFamily: "var(--font-heading)",
            }}
          >
            How It <span className="gradient-text">Works</span>
          </h2>
          <p style={{ color: "var(--color-text-secondary)", marginBottom: 60, fontSize: "1.1rem" }}>
            Three simple steps to find your perfect property
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 40 }}>
            {[
              { step: "01", title: "Ask Anything", desc: "Type your real estate question in natural language" },
              { step: "02", title: "AI Analyzes", desc: "Our agent searches, calculates, and gathers data" },
              { step: "03", title: "Get Results", desc: "Receive detailed, actionable insights instantly" },
            ].map((item) => (
              <div key={item.step} style={{ textAlign: "center" }}>
                <div
                  className="gradient-text"
                  style={{
                    fontSize: "3rem",
                    fontWeight: 800,
                    fontFamily: "var(--font-heading)",
                    marginBottom: 16,
                  }}
                >
                  {item.step}
                </div>
                <h3 style={{ fontSize: "1.2rem", fontWeight: 700, marginBottom: 8 }}>{item.title}</h3>
                <p style={{ color: "var(--color-text-secondary)", fontSize: "0.95rem" }}>{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{ padding: "100px 1.5rem", textAlign: "center" }}>
        <div style={{ maxWidth: 600, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: "clamp(1.8rem, 4vw, 2.5rem)",
              fontWeight: 800,
              marginBottom: 16,
              fontFamily: "var(--font-heading)",
            }}
          >
            Ready to Find Your <span className="gradient-text">Dream Home</span>?
          </h2>
          <p style={{ color: "var(--color-text-secondary)", marginBottom: 40, fontSize: "1.1rem" }}>
            Start a conversation with our AI agent and discover properties tailored to you.
          </p>
          <a href="/chat" className="btn-primary" style={{ padding: "16px 40px", fontSize: "1.05rem" }}>
            🚀 Start Free Chat
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer
        style={{
          borderTop: "1px solid var(--color-border)",
          padding: "40px 1.5rem",
          textAlign: "center",
          color: "var(--color-text-muted)",
          fontSize: "0.85rem",
        }}
      >
        <p>
          © 2025 RealEstateAI. Built with ❤️ using Next.js, FastAPI, and GPT-4o.
        </p>
      </footer>
    </>
  );
}
