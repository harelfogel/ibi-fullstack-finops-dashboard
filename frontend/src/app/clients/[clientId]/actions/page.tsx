"use client";

import { useParams } from "next/navigation";
import { ViolationsList } from "@/components/actions/ViolationsList";
import { InsightsPanel } from "@/components/actions/InsightsPanel";
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

  const isLoading = violationsLoading || insightLoading;

  if (isLoading) {
    return (
      <div className="flex justify-center py-16">
        <Spinner className="h-8 w-8" />
      </div>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      {/* Violations column */}
      <div>
        <h2 className="mb-4 text-lg font-semibold text-white">
          Rule Violations
          {violations && violations.length > 0 && (
            <span className="ml-2 text-sm font-normal text-slate-400">
              ({violations.length})
            </span>
          )}
        </h2>
        {violations && <ViolationsList violations={violations} />}
      </div>

      {/* Insights column */}
      <div>
        <h2 className="mb-4 text-lg font-semibold text-white">
          AI Insights
        </h2>
        {insight && <InsightsPanel insight={insight} />}
      </div>
    </div>
  );
}
