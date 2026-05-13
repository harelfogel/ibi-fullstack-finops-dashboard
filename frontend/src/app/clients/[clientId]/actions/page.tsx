"use client";

import { useParams } from "next/navigation";
import { ViolationsList } from "@/components/actions/ViolationsList";
import { InsightsPanel } from "@/components/actions/InsightsPanel";
import { InsightsSkeleton } from "@/components/actions/InsightsSkeleton";
import { Spinner } from "@/components/ui/Spinner";
import { useViolations } from "@/lib/hooks/useViolations";
import { useInsights } from "@/lib/hooks/useInsights";

export default function ActionsPage() {
  const params = useParams();
  const clientId = params.clientId as string;

  const {
    data: violations,
    isLoading: violationsLoading,
  } = useViolations(clientId);

  const {
    data: insight,
    isLoading: insightLoading,
  } = useInsights(clientId);

  return (
    <div className="grid gap-6 lg:grid-cols-2 lg:items-start">
      {/* Violations column */}
      <div className="lg:sticky lg:top-6">
        <h2 className="mb-4 text-lg font-semibold text-white">
          Rule Violations
          {violations && violations.length > 0 && (
            <span className="ml-2 text-sm font-normal text-slate-400">
              ({violations.length})
            </span>
          )}
        </h2>
        {violationsLoading ? (
          <div className="flex justify-center py-16">
            <Spinner className="h-8 w-8" />
          </div>
        ) : (
          violations && <ViolationsList violations={violations} />
        )}
      </div>

      {/* Insights column */}
      <div>
        <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold">
          <svg className="h-5 w-5 text-violet-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z" />
          </svg>
          <span className="bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">AI Insights</span>
        </h2>
        {insightLoading ? (
          <InsightsSkeleton />
        ) : (
          insight && <InsightsPanel insight={insight} />
        )}
      </div>
    </div>
  );
}
