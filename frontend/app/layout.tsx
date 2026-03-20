import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";
import { Geist } from "next/font/google";
import { cn } from "@/lib/utils";

const geist = Geist({subsets:['latin'],variable:'--font-sans'});

export const metadata: Metadata = {
  title: "VC Aggregator",
  description: "Browse startup portfolios",
};

export default function RootLayout({
  children,
}: Readonly<{children: React.ReactNode}>) {
  return (
    <html lang="en" className={cn("font-sans", geist.variable)}>
      <body className={`antialiased flex flex-col min-h-screen`}>
        <header className="border-b sticky top-0 bg-background z-10">
          <div className="container mx-auto px-4 h-16 flex items-center justify-between">
            <Link href="/" className="font-bold text-xl tracking-tight">
              VC Aggregator
            </Link>
            <nav className="flex items-center gap-6 text-sm font-medium">
              <Link href="/" className="hover:text-primary">Startups</Link>
              <Link href="/investors" className="hover:text-primary">Investors</Link>
            </nav>
          </div>
        </header>
        <main className="flex-1 bg-muted/20">
          {children}
        </main>
      </body>
    </html>
  );
}
