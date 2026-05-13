"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/Card";

const dots = [0, 1, 2];

export function InsightsSkeleton() {
  return (
    <div className="space-y-4">
      {/* Main AI loading card */}
      <div className="relative overflow-hidden rounded-xl border border-cyan-500/20 bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 p-6">
        {/* Animated glow backgrounds */}
        <motion.div
          className="pointer-events-none absolute -top-24 -right-24 h-48 w-48 rounded-full bg-cyan-500/10 blur-3xl"
          animate={{ opacity: [0.2, 0.5, 0.2] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="pointer-events-none absolute -bottom-24 -left-24 h-48 w-48 rounded-full bg-violet-500/10 blur-3xl"
          animate={{ opacity: [0.2, 0.5, 0.2] }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1,
          }}
        />

        <div className="relative flex flex-col items-center py-6 text-center">
          {/* Animated brain/spark icon */}
          <motion.div
            className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-violet-500 shadow-lg shadow-cyan-500/25"
            animate={{ scale: [1, 1.08, 1] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          >
            <svg
              className="h-6 w-6 text-white"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z"
              />
            </svg>
          </motion.div>

          <p className="mb-1 text-sm font-semibold bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">
            AI is analyzing this portfolio
          </p>
          <p className="text-xs text-slate-500">
            Evaluating positions, risks &amp; violations
          </p>

          {/* Animated dots */}
          <div className="mt-4 flex gap-1.5">
            {dots.map((i) => (
              <motion.div
                key={i}
                className="h-1.5 w-1.5 rounded-full bg-cyan-400"
                animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1.2, 0.8] }}
                transition={{
                  duration: 1.2,
                  repeat: Infinity,
                  ease: "easeInOut",
                  delay: i * 0.2,
                }}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Skeleton cards */}
      <Card>
        <div className="animate-pulse">
          <div className="mb-3 h-4 w-24 rounded bg-slate-800" />
          <div className="flex items-center gap-4">
            <div className="h-16 w-16 rounded-full bg-slate-800" />
            <div className="space-y-2">
              <div className="h-4 w-20 rounded bg-slate-800" />
              <div className="h-3 w-32 rounded bg-slate-800" />
            </div>
          </div>
        </div>
      </Card>

      <Card>
        <div className="animate-pulse">
          <div className="mb-3 h-4 w-32 rounded bg-slate-800" />
          <div className="space-y-3">
            <div className="h-3 w-full rounded bg-slate-800" />
            <div className="h-3 w-5/6 rounded bg-slate-800" />
            <div className="h-3 w-4/6 rounded bg-slate-800" />
          </div>
        </div>
      </Card>
    </div>
  );
}
