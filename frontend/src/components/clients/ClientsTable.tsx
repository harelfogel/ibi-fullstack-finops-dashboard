"use client";

import Link from "next/link";
import { useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { formatCurrency, pnlColor, pnlSign } from "@/lib/utils/format";
import { useDeleteClient } from "@/lib/hooks/useDeleteClient";
import { useToast } from "@/lib/providers/ToastProvider";
import { ClientSummary } from "@/types/client";

interface ClientsTableProps {
  clients: ClientSummary[];
}

type SortKey = "client_id" | "total_value" | "total_realized_pnl" | "violation_count";

export function ClientsTable({ clients }: ClientsTableProps) {
  const [sortKey, setSortKey] = useState<SortKey>("client_id");
  const [sortAsc, setSortAsc] = useState(true);
  const [search, setSearch] = useState("");
  const [confirmingId, setConfirmingId] = useState<string | null>(null);
  const deleteClient = useDeleteClient();
  const { addToast } = useToast();

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

  const handleDelete = async (clientId: string) => {
    try {
      await deleteClient.mutateAsync(clientId);
      addToast("success", `Client ${clientId} deleted`);
    } catch (err) {
      addToast("error", err instanceof Error ? err.message : "Delete failed");
    }
    setConfirmingId(null);
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
                  {formatCurrency(Number(client.total_value))}
                </td>
                <td className={`px-4 py-3 font-mono ${pnlColor(Number(client.total_realized_pnl))}`}>
                  {pnlSign(Number(client.total_realized_pnl))}
                  {formatCurrency(Number(client.total_realized_pnl))}
                </td>
                <td className="px-4 py-3">
                  {client.violation_count > 0 ? (
                    <Badge variant="error">{client.violation_count}</Badge>
                  ) : (
                    <Badge variant="success">Clean</Badge>
                  )}
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <Link
                      href={`/clients/${client.client_id}/portfolio`}
                      title="View portfolio"
                      className="rounded-lg bg-slate-800 p-2 text-cyan-400 transition-colors hover:bg-slate-700"
                    >
                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                      </svg>
                    </Link>
                    {confirmingId === client.client_id ? (
                      <div className="flex items-center gap-1">
                        <button
                          onClick={() => handleDelete(client.client_id)}
                          disabled={deleteClient.isPending}
                          className="rounded-lg bg-red-600 px-2.5 py-1.5 text-xs font-medium text-white transition-colors hover:bg-red-500 disabled:opacity-50"
                        >
                          {deleteClient.isPending ? "..." : "Confirm"}
                        </button>
                        <button
                          onClick={() => setConfirmingId(null)}
                          className="rounded-lg bg-slate-800 px-2.5 py-1.5 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-700"
                        >
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => setConfirmingId(client.client_id)}
                        title="Delete client"
                        className="rounded-lg bg-slate-800 p-2 text-red-400 transition-colors hover:bg-red-500/10"
                      >
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                        </svg>
                      </button>
                    )}
                  </div>
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
