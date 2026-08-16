"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import { authApi } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await authApi.register({ full_name: fullName, email, password });
      localStorage.setItem("access_token", response.access_token);
      localStorage.setItem("refresh_token", response.refresh_token);
      localStorage.setItem("user", JSON.stringify(response.user));
      router.push("/chat");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "80px 24px",
        }}
      >
        <div
          className="glass-card animate-fade-in"
          style={{ padding: 40, maxWidth: 420, width: "100%" }}
        >
          <div style={{ textAlign: "center", marginBottom: 32 }}>
            <div style={{ fontSize: "2.5rem", marginBottom: 12 }}>🚀</div>
            <h1
              style={{
                fontSize: "1.5rem",
                fontWeight: 700,
                fontFamily: "var(--font-heading)",
                marginBottom: 8,
              }}
            >
              Create Account
            </h1>
            <p style={{ color: "var(--color-text-muted)", fontSize: "0.9rem" }}>
              Start your AI-powered real estate journey
            </p>
          </div>

          {error && (
            <div
              style={{
                padding: "10px 14px",
                borderRadius: 10,
                background: "rgba(239, 68, 68, 0.1)",
                border: "1px solid rgba(239, 68, 68, 0.3)",
                color: "#ef4444",
                fontSize: "0.85rem",
                marginBottom: 20,
              }}
            >
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <div>
              <label style={{ fontSize: "0.85rem", color: "var(--color-text-secondary)", marginBottom: 6, display: "block" }}>
                Full Name
              </label>
              <input
                className="input"
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="John Doe"
              />
            </div>
            <div>
              <label style={{ fontSize: "0.85rem", color: "var(--color-text-secondary)", marginBottom: 6, display: "block" }}>
                Email
              </label>
              <input
                className="input"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
              />
            </div>
            <div>
              <label style={{ fontSize: "0.85rem", color: "var(--color-text-secondary)", marginBottom: 6, display: "block" }}>
                Password
              </label>
              <input
                className="input"
                type="password"
                required
                minLength={8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••  (min 8 characters)"
              />
            </div>
            <button
              type="submit"
              className="btn-primary"
              disabled={loading}
              style={{
                padding: "14px",
                fontSize: "1rem",
                marginTop: 8,
                opacity: loading ? 0.7 : 1,
              }}
            >
              {loading ? "Creating account..." : "Create Account"}
            </button>
          </form>

          <p
            style={{
              textAlign: "center",
              marginTop: 24,
              fontSize: "0.85rem",
              color: "var(--color-text-muted)",
            }}
          >
            Already have an account?{" "}
            <a href="/auth/login" style={{ color: "var(--color-accent)", fontWeight: 600 }}>
              Sign In
            </a>
          </p>
        </div>
      </div>
    </>
  );
}
