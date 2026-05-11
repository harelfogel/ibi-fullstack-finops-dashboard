"use client";

import Link from "next/link";
import { useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { formatCurrency, pnlColor, pnlSign } from "@/lib/utils/format";
import { ClientSummary } from "@/types/client";

interface ClientsTableProps {
  clients: ClientSummary[];
}

type SortKey = "client_id" | "total_value" | "total_realized_pnl" | "violation_count";

export function ClientsTable({ clients }: ClientsTableProps) {
  const [sortKey, setSortKey] = useState<SortKey>("client_id");
  const [sortAsc, setSortAsc] = useState(true);
  const [search, setSearch] = useState("");

  const filtered = clients.filter((c) =>
    c.client_id.toLowerCase().includes(search.toLowerCase()),
  );

  const sorted = [...filtered].sort((a, b) => {
    const dir = sortAsc ? 1 : -1;
    if (sortKey === "client_id") return a.client_id.localeCompare(b.client_id) * dir;
    return ((a[sortKey] as number) - (b[sortKey] as number)) * dir;
  });

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) setSortAsc(!sortAsc);
    else {
      setSortKey(key);
      setSortAsc(true);
    }
  };

  const SortHeader = ({ label, sortKeyVal }: { label: string; sortKeyVal: SortKey }) => (
    <th
      className="cursor-pointer px-4 py-3 text-left font-medium text-slate-400 hover:text-slate-200"
      onClick={() => toggleSort(sortKeyVal)}
    >
      {label}
      {sortKey === sortKeyVal && (
        <span className="ml-1">{sortAsc ? "\u2191" : "\u2193"}</span>
      )}
    </th>
  );

  return (
    <div>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search clients..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full max-w-sm rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
        />
      </div>
      <div className="overflow-hidden rounded-xl border border-slate-800">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-900">
              <SortHeader label="Client ID" sortKeyVal="client_id" />
              <th className="px-4 py-3 text-left font-medium text-slate-400">
                Positions
              </th>
              <SortHeader label="Portfolio Value" sortKeyVal="total_value" />
              <SortHeader label="Realized P&L" sortKeyVal="total_realized_pnl" />
              <SortHeader label="Violations" sortKeyVal="violation_count" />
              <th className="px-4 py-3 text-left font-medium text-slate-400">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {sorted.map((client) => (
              <tr
                key={client.client_id}
                className="bg-slate-950 transition-colors hover:bg-slate-900/50"
              >
                <td className="px-4 py-3 font-mono font-medium text-cyan-400">
                  {client.client_id}
                </td>
                <td className="px-4 py-3 font-mono text-slate-300">
                  {client.position_count}
                </td>
                <td className="px-4 py-3 font-mono text-slate-300">
                  {formatCurrency(client.total_value)}
                </td>
                <td className={`px-4 py-3 font-mono ${pnlColor(client.total_realized_pnl)}`}>
                  {pnlSign(client.total_realized_pnl)}
                  {formatCurrency(client.total_realized_pnl)}
                </td>
                <td className="px-4 py-3">
                  {client.violation_count > 0 ? (
                    <Badge variant="error">{client.violation_count}</Badge>
                  ) : (
                    <Badge variant="success">Clean</Badge>
                  )}
                </td>
                <td className="px-4 py-3">
                  <Link
                    href={`/clients/${client.client_id}/portfolio`}
                    className="rounded-lg bg-slate-800 px-3 py-1.5 text-xs font-medium text-cyan-400 transition-colors hover:bg-slate-700"
                  >
                    View
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {sorted.length === 0 && (
          <div className="py-8 text-center text-sm text-slate-500">
            No clients found
          </div>
        )}
      </div>
    </div>
  );
}
