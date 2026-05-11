import { Card } from "@/components/ui/Card";
import { Insight } from "@/types/insight";

export function InsightsPanel({ insight }: { insight: Insight }) {
  return (
    <div className="space-y-4">
      {/* AI Summary Card with glow effect */}
      <div className="relative overflow-hidden rounded-xl border border-cyan-500/20 bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 p-6">
        {/* Glow background */}
        <div className="pointer-events-none absolute -top-24 -right-24 h-48 w-48 rounded-full bg-cyan-500/10 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-24 -left-24 h-48 w-48 rounded-full bg-violet-500/10 blur-3xl" />

        <div className="relative">
          <div className="mb-3 flex items-center gap-2">
            <div className="flex h-6 w-6 items-center justify-center rounded-md bg-gradient-to-br from-cyan-500 to-violet-500">
              <svg className="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
              </svg>
            </div>
            <h3 className="text-sm font-semibold text-cyan-400">AI Portfolio Analysis</h3>
          </div>
          <p className="text-sm leading-relaxed text-slate-300">{insight.summary}</p>
        </div>
      </div>

      {/* Risk Score */}
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
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke={insight.risk_score <= 3 ? "#10b981" : insight.risk_score <= 6 ? "#f59e0b" : "#ef4444"}
                strokeWidth="3"
                strokeDasharray={`${(insight.risk_score / 10) * 100}, 100`}
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

      {/* Recommendations */}
      {insight.recommendations.length > 0 && (
        <Card>
          <h4 className="mb-3 text-sm font-medium text-slate-400">
            Recommendations
          </h4>
          <ul className="space-y-2">
            {insight.recommendations.map((rec, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-300">
                <span className="mt-0.5 text-cyan-500">&#x2022;</span>
                {rec}
              </li>
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
              <span
                key={i}
                className="rounded-lg bg-slate-800 px-3 py-1.5 text-xs font-medium text-slate-300"
              >
                {h}
              </span>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
