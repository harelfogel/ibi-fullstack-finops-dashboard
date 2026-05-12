"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { useUploadModal } from "@/app/AppShell";
import { useClients } from "@/lib/hooks/useClients";
import { formatCurrency } from "@/lib/utils/format";

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
};

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const features = [
  {
    title: "Upload & Process",
    description: "Drag-and-drop CSV/XLSX files with instant validation and error reporting.",
    icon: UploadFeatureIcon,
  },
  {
    title: "Portfolio Analysis",
    description: "FIFO-based position tracking with realized and unrealized P&L.",
    icon: ChartIcon,
  },
  {
    title: "Compliance Monitoring",
    description: "Automatic detection of short selling, concentration risk, and day trading.",
    icon: ShieldIcon,
  },
  {
    title: "AI Insights",
    description: "LLM-generated analysis of portfolio composition and risk factors.",
    icon: SparklesIcon,
  },
];

export default function HomePage() {
  const { openUploadModal } = useUploadModal();
  const { data: clients } = useClients();
  const hasData = clients && clients.length > 0;

  const totalPositions = hasData
    ? clients.reduce((sum, c) => sum + Number(c.position_count), 0)
    : 0;
  const totalValue = hasData
    ? clients.reduce((sum, c) => sum + Number(c.total_value), 0)
    : 0;

  return (
    <div className="mx-auto max-w-4xl py-8">
      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="space-y-16"
      >
        {/* Hero */}
        <motion.div variants={fadeUp} className="flex flex-col items-center text-center">
          {/* Animated logo */}
          <div className="mb-8 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-violet-500 animate-glow">
            <span className="text-2xl font-bold text-white">IBI</span>
          </div>

          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            <span className="bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">
              Clarity
            </span>
          </h1>
          <p className="mt-4 max-w-lg text-lg text-slate-400">
            Financial operations intelligence for modern portfolios
          </p>

          {/* CTAs */}
          <div className="mt-8 flex items-center gap-4">
            {hasData ? (
              <Link
                href="/clients"
                className="rounded-lg bg-cyan-600 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-cyan-500"
              >
                View Dashboard
              </Link>
            ) : (
              <button
                onClick={openUploadModal}
                className="rounded-lg bg-cyan-600 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-cyan-500"
              >
                Upload Transactions
              </button>
            )}
          </div>
        </motion.div>

        {/* Quick stats */}
        {hasData && (
          <motion.div variants={fadeUp}>
            <div className="grid grid-cols-3 gap-4">
              <StatCard label="Clients" value={String(clients.length)} />
              <StatCard label="Positions" value={String(totalPositions)} />
              <StatCard label="Portfolio Value" value={formatCurrency(totalValue)} />
            </div>
          </motion.div>
        )}

        {/* Feature cards */}
        <motion.div variants={fadeUp}>
          <div className="grid gap-4 sm:grid-cols-2">
            {features.map((f) => (
              <div
                key={f.title}
                className="rounded-xl border border-slate-800 bg-slate-900/50 p-5"
              >
                <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-slate-800 text-cyan-400">
                  <f.icon className="h-5 w-5" />
                </div>
                <h3 className="text-sm font-semibold text-white">{f.title}</h3>
                <p className="mt-1 text-sm text-slate-500">{f.description}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4 text-center">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 text-lg font-semibold text-white font-mono">{value}</p>
    </div>
  );
}

/* ---- Icons ---- */

function UploadFeatureIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
    </svg>
  );
}

function ChartIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
    </svg>
  );
}

function ShieldIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  );
}

function SparklesIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
    </svg>
  );
}
