"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/Card";
import { Insight } from "@/types/insight";

export function InsightsPanel({ insight }: { insight: Insight }) {
  const riskPct = (insight.risk_score / 10) * 100;
  const riskColor =
    insight.risk_score <= 3
      ? "#10b981"
      : insight.risk_score <= 6
        ? "#f59e0b"
        : "#ef4444";

  return (
    <div className="space-y-4">
      {/* AI Summary Card with animated glow effect */}
      <div className="ai-card relative overflow-hidden rounded-xl border border-cyan-500/20 bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 p-6">
        {/* Animated glow backgrounds */}
        <motion.div
          className="pointer-events-none absolute -top-24 -right-24 h-48 w-48 rounded-full bg-cyan-500/10 blur-3xl"
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="pointer-events-none absolute -bottom-24 -left-24 h-48 w-48 rounded-full bg-violet-500/10 blur-3xl"
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 1.5 }}
        />

        <div className="relative">
          <div className="mb-3 flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-to-br from-cyan-500 to-violet-500 shadow-lg shadow-cyan-500/20">
              <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z" />
              </svg>
            </div>
            <h3 className="text-sm font-semibold bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">AI Portfolio Analysis</h3>
          </div>
          <p className="text-sm leading-relaxed text-slate-300">{insight.summary}</p>
        </div>
      </div>

      {/* Risk Score with animated ring */}
      <Card>
        <h4 className="mb-3 text-sm font-medium text-slate-400">Risk Score</h4>
        <div className="flex items-center gap-4">
          <div className="relative h-16 w-16">
            <svg className="h-16 w-16 -rotate-90" viewBox="0 0 36 36">
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="#1e293b"
                strokeWidth="3"
              />
              <motion.path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke={riskColor}
                strokeWidth="3"
                initial={{ strokeDasharray: "0, 100" }}
                animate={{ strokeDasharray: `${riskPct}, 100` }}
                transition={{ duration: 1, ease: "easeOut" }}
              />
            </svg>
            <span className="absolute inset-0 flex items-center justify-center text-lg font-bold text-white font-mono">
              {insight.risk_score}
            </span>
          </div>
          <div>
            <p className="text-sm font-medium text-white">
              {insight.risk_score <= 3 ? "Low Risk" : insight.risk_score <= 6 ? "Medium Risk" : "High Risk"}
            </p>
            <p className="text-xs text-slate-500">Scale: 1 (low) to 10 (high)</p>
          </div>
        </div>
      </Card>

      {/* Recommendations with staggered fade-in */}
      {insight.recommendations.length > 0 && (
        <Card>
          <h4 className="mb-3 text-sm font-medium text-slate-400">
            Recommendations
          </h4>
          <ul className="space-y-2">
            {insight.recommendations.map((rec, i) => (
              <motion.li
                key={i}
                className="flex gap-2 text-sm text-slate-300"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * i, duration: 0.3 }}
              >
                <span className="mt-0.5 text-cyan-500">&#x2022;</span>
                {rec}
              </motion.li>
            ))}
          </ul>
        </Card>
      )}

      {/* Highlights */}
      {insight.highlights.length > 0 && (
        <Card>
          <h4 className="mb-3 text-sm font-medium text-slate-400">
            Key Highlights
          </h4>
          <div className="flex flex-wrap gap-2">
            {insight.highlights.map((h, i) => (
              <motion.span
                key={i}
                className="rounded-lg bg-slate-800 px-3 py-1.5 text-xs font-medium text-slate-300"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 * i, duration: 0.3 }}
              >
                {h}
              </motion.span>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
