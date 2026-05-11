import { Card } from "@/components/ui/Card";
import { UploadResult } from "@/types/transaction";

interface ValidationSummaryProps {
  result: UploadResult;
}

export function ValidationSummary({ result }: ValidationSummaryProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-3">
      <Card>
        <p className="text-sm text-slate-400">Total Rows</p>
        <p className="mt-1 text-2xl font-bold text-white font-mono">
          {result.total_rows}
        </p>
      </Card>
      <Card>
        <p className="text-sm text-slate-400">Valid</p>
        <p className="mt-1 text-2xl font-bold text-emerald-400 font-mono">
          {result.valid_rows}
        </p>
      </Card>
      <Card>
        <p className="text-sm text-slate-400">Errors</p>
        <p className="mt-1 text-2xl font-bold font-mono text-red-400">
          {result.error_rows}
        </p>
      </Card>
    </div>
  );
}
