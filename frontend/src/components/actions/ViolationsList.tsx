import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { formatDate } from "@/lib/utils/format";
import { Violation } from "@/types/violation";

const typeLabels: Record<string, string> = {
  short_selling: "Short Selling",
  concentration_risk: "Concentration Risk",
  day_trading: "Day Trading",
};

export function ViolationsList({ violations }: { violations: Violation[] }) {
  if (violations.length === 0) {
    return (
      <Card className="text-center">
        <div className="py-6">
          <svg className="mx-auto mb-3 h-10 w-10 text-emerald-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-sm text-slate-400">No violations detected</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {violations.map((v) => (
        <Card
          key={v.id}
          className={`border-l-4 ${v.severity === "error" ? "border-l-red-500" : "border-l-amber-500"}`}
        >
          <div className="flex flex-wrap items-start justify-between gap-2">
            <div className="flex-1">
              <div className="mb-1 flex items-center gap-2">
                <Badge variant={v.severity === "error" ? "error" : "warning"}>
                  {v.severity.toUpperCase()}
                </Badge>
                <Badge variant="info">
                  {typeLabels[v.violation_type] || v.violation_type}
                </Badge>
              </div>
              <p className="text-sm text-slate-300">{v.message}</p>
              {v.transaction_id && (
                <p className="mt-1 text-xs text-slate-500">
                  Transaction: {v.transaction_id}
                </p>
              )}
            </div>
            <span className="text-xs text-slate-600">
              {formatDate(v.detected_at)}
            </span>
          </div>
        </Card>
      ))}
    </div>
  );
}
