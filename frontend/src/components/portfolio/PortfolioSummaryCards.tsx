import { Card } from "@/components/ui/Card";
import { formatCurrency, pnlColor, pnlSign } from "@/lib/utils/format";
import { Portfolio } from "@/types/portfolio";

export function PortfolioSummaryCards({ portfolio }: { portfolio: Portfolio }) {
  return (
    <div className="grid gap-4 sm:grid-cols-3">
      <Card>
        <p className="text-sm text-slate-400">Total Value</p>
        <p className="mt-1 text-2xl font-bold text-white font-mono">
          {formatCurrency(portfolio.total_value)}
        </p>
      </Card>
      <Card>
        <p className="text-sm text-slate-400">Realized P&L</p>
        <p
          className={`mt-1 text-2xl font-bold font-mono ${pnlColor(portfolio.total_realized_pnl)}`}
        >
          {pnlSign(portfolio.total_realized_pnl)}
          {formatCurrency(portfolio.total_realized_pnl)}
        </p>
      </Card>
      <Card>
        <p className="text-sm text-slate-400">Unrealized P&L</p>
        <p
          className={`mt-1 text-2xl font-bold font-mono ${pnlColor(portfolio.total_unrealized_pnl)}`}
        >
          {pnlSign(portfolio.total_unrealized_pnl)}
          {formatCurrency(portfolio.total_unrealized_pnl)}
        </p>
      </Card>
    </div>
  );
}
