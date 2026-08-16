"use client";

import { useState } from "react";
import Link from "next/link";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 1030,
        background: "rgba(15, 23, 42, 0.85)",
        backdropFilter: "blur(16px)",
        WebkitBackdropFilter: "blur(16px)",
        borderBottom: "1px solid rgba(148, 163, 184, 0.1)",
      }}
    >
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "0 1.5rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          height: 64,
        }}
      >
        {/* Logo */}
        <Link href="/" style={{ display: "flex", alignItems: "center", gap: 10, textDecoration: "none" }}>
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 10,
              background: "linear-gradient(135deg, #14b8a6 0%, #0ea5e9 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 18,
            }}
          >
            🏠
          </div>
          <span
            style={{
              fontSize: "1.25rem",
              fontWeight: 700,
              fontFamily: "var(--font-heading)",
              color: "var(--color-text-primary)",
            }}
          >
            RealEstate<span style={{ color: "var(--color-accent)" }}>AI</span>
          </span>
        </Link>

        {/* Desktop Nav */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 32,
          }}
          className="desktop-nav"
        >
          <Link
            href="/chat"
            style={{
              color: "var(--color-text-secondary)",
              fontSize: "0.9rem",
              fontWeight: 500,
              transition: "color 0.2s",
            }}
          >
            💬 AI Chat
          </Link>
          <Link
            href="/properties"
            style={{
              color: "var(--color-text-secondary)",
              fontSize: "0.9rem",
              fontWeight: 500,
              transition: "color 0.2s",
            }}
          >
            🏘️ Properties
          </Link>
          <Link
            href="/dashboard"
            style={{
              color: "var(--color-text-secondary)",
              fontSize: "0.9rem",
              fontWeight: 500,
              transition: "color 0.2s",
            }}
          >
            📊 Dashboard
          </Link>
          <Link href="/auth/login" className="btn-secondary" style={{ padding: "6px 18px", fontSize: "0.85rem" }}>
            Sign In
          </Link>
          <Link href="/auth/register" className="btn-primary" style={{ padding: "6px 18px", fontSize: "0.85rem" }}>
            Get Started
          </Link>
        </div>

        {/* Mobile menu button */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          style={{
            display: "none",
            background: "none",
            border: "none",
            color: "var(--color-text-primary)",
            fontSize: "1.5rem",
            cursor: "pointer",
          }}
          className="mobile-menu-btn"
        >
          {menuOpen ? "✕" : "☰"}
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div
          style={{
            padding: "1rem 1.5rem",
            display: "flex",
            flexDirection: "column",
            gap: 12,
            borderTop: "1px solid var(--color-border)",
          }}
        >
          <Link href="/chat" onClick={() => setMenuOpen(false)} style={{ color: "var(--color-text-secondary)", padding: "8px 0" }}>
            💬 AI Chat
          </Link>
          <Link href="/properties" onClick={() => setMenuOpen(false)} style={{ color: "var(--color-text-secondary)", padding: "8px 0" }}>
            🏘️ Properties
          </Link>
          <Link href="/dashboard" onClick={() => setMenuOpen(false)} style={{ color: "var(--color-text-secondary)", padding: "8px 0" }}>
            📊 Dashboard
          </Link>
          <Link href="/auth/login" className="btn-secondary" style={{ textAlign: "center", padding: "10px" }}>
            Sign In
          </Link>
          <Link href="/auth/register" className="btn-primary" style={{ textAlign: "center", padding: "10px" }}>
            Get Started
          </Link>
        </div>
      )}

      <style>{`
        @media (max-width: 768px) {
          .desktop-nav { display: none !important; }
          .mobile-menu-btn { display: block !important; }
        }
      `}</style>
    </nav>
  );
}
