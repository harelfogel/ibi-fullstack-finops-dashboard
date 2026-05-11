import { formatCurrency, formatNumber, pnlColor, pnlSign } from "@/lib/utils/format";
import { Position } from "@/types/portfolio";

interface HoldingsTableProps {
  positions: Position[];
}

export function HoldingsTable({ positions }: HoldingsTableProps) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-800">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-800 bg-slate-900">
            <th className="px-4 py-3 text-left font-medium text-slate-400">
              ISIN
            </th>
            <th className="px-4 py-3 text-right font-medium text-slate-400">
              Quantity
            </th>
            <th className="px-4 py-3 text-right font-medium text-slate-400">
              Avg Cost
            </th>
            <th className="px-4 py-3 text-right font-medium text-slate-400">
              Market Value
            </th>
            <th className="px-4 py-3 text-right font-medium text-slate-400">
              Realized P&L
            </th>
            <th className="px-4 py-3 text-right font-medium text-slate-400">
              Unrealized P&L
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {positions.map((pos) => (
            <tr
              key={pos.isin}
              className="bg-slate-950 transition-colors hover:bg-slate-900/50"
            >
              <td className="px-4 py-3 font-mono font-medium text-cyan-400">
                {pos.isin}
              </td>
              <td className="px-4 py-3 text-right font-mono text-slate-300">
                {formatNumber(pos.current_quantity, 0)}
              </td>
              <td className="px-4 py-3 text-right font-mono text-slate-300">
                {formatCurrency(pos.average_cost)}
              </td>
              <td className="px-4 py-3 text-right font-mono text-slate-300">
                {formatCurrency(pos.market_value)}
              </td>
              <td
                className={`px-4 py-3 text-right font-mono ${pnlColor(pos.realized_pnl)}`}
              >
                {pnlSign(pos.realized_pnl)}
                {formatCurrency(pos.realized_pnl)}
              </td>
              <td
                className={`px-4 py-3 text-right font-mono ${pnlColor(pos.unrealized_pnl)}`}
              >
                {pnlSign(pos.unrealized_pnl)}
                {formatCurrency(pos.unrealized_pnl)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
