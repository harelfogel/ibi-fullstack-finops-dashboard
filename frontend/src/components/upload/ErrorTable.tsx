import { UploadError } from "@/types/transaction";

interface ErrorTableProps {
  errors: UploadError[];
}

export function ErrorTable({ errors }: ErrorTableProps) {
  if (errors.length === 0) return null;

  return (
    <div className="overflow-hidden rounded-xl border border-slate-800">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-800 bg-slate-900">
            <th className="px-4 py-3 text-left font-medium text-slate-400">
              Row
            </th>
            <th className="px-4 py-3 text-left font-medium text-slate-400">
              Field
            </th>
            <th className="px-4 py-3 text-left font-medium text-slate-400">
              Error
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {errors.map((err, i) => (
            <tr key={i} className="bg-slate-950 hover:bg-slate-900/50">
              <td className="px-4 py-3 font-mono text-slate-300">{err.row}</td>
              <td className="px-4 py-3 text-amber-400">{err.field}</td>
              <td className="px-4 py-3 text-slate-400">{err.message}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
