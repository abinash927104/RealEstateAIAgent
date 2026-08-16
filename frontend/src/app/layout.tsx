import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RealEstateAI — AI-Powered Property Assistant",
  description: "Find your dream home with AI. Search properties, calculate mortgages, analyze ROI, and get market insights powered by advanced AI.",
  keywords: "real estate, AI, property search, mortgage calculator, investment analysis, market trends",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body>
        {children}
      </body>
    </html>
  );
}
