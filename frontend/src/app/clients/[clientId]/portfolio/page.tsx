"use client";

import { useParams } from "next/navigation";
import { PortfolioSummaryCards } from "@/components/portfolio/PortfolioSummaryCards";
import { HoldingsTable } from "@/components/portfolio/HoldingsTable";
import { Spinner } from "@/components/ui/Spinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { usePortfolio } from "@/lib/hooks/usePortfolio";

export default function PortfolioPage() {
  const params = useParams();
  const clientId = params.clientId as string;
  const { data: portfolio, isLoading, error } = usePortfolio(clientId);

  if (isLoading) {
    return (
      <div className="flex justify-center py-16">
        <Spinner className="h-8 w-8" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
        Failed to load portfolio: {error.message}
      </div>
    );
  }

  if (!portfolio || portfolio.positions.length === 0) {
    return (
      <EmptyState
        title="No Positions"
        description="This client has no portfolio positions yet."
      />
    );
  }

  return (
    <div className="space-y-6">
      <PortfolioSummaryCards portfolio={portfolio} />
      <div>
        <h2 className="mb-3 text-lg font-semibold text-white">Holdings</h2>
        <HoldingsTable positions={portfolio.positions} />
      </div>
    </div>
  );
}
