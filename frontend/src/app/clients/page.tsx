"use client";

import { PageHeader } from "@/components/layout/PageHeader";
import { ClientsTable } from "@/components/clients/ClientsTable";
import { Spinner } from "@/components/ui/Spinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { useClients } from "@/lib/hooks/useClients";
import { useUploadModal } from "@/app/AppShell";

export default function ClientsPage() {
  const { data: clients, isLoading, error } = useClients();
  const { openUploadModal } = useUploadModal();
  const hasClients = clients && clients.length > 0;

  return (
    <div>
      <PageHeader
        title="Clients"
        description="Overview of all clients with portfolio summaries and violation status."
        actions={
          hasClients ? (
            <button
              onClick={openUploadModal}
              className="flex items-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-cyan-500"
            >
              <UploadIcon className="h-4 w-4" />
              Upload Transactions
            </button>
          ) : undefined
        }
      />

      {isLoading && (
        <div className="flex justify-center py-16">
          <Spinner className="h-8 w-8" />
        </div>
      )}

      {error && (
        <div className="rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
          Failed to load clients: {error.message}
        </div>
      )}

      {clients && clients.length === 0 && (
        <EmptyState
          title="No Clients Yet"
          description="Upload a transaction file to get started."
          action={{ label: "Upload Transactions", onClick: openUploadModal }}
        />
      )}

      {clients && clients.length > 0 && <ClientsTable clients={clients} />}
    </div>
  );
}

function UploadIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
    </svg>
  );
}
