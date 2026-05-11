"use client";

import { PageHeader } from "@/components/layout/PageHeader";
import { ClientsTable } from "@/components/clients/ClientsTable";
import { Spinner } from "@/components/ui/Spinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { useClients } from "@/lib/hooks/useClients";

export default function ClientsPage() {
  const { data: clients, isLoading, error } = useClients();

  return (
    <div>
      <PageHeader
        title="Clients"
        description="Overview of all clients with portfolio summaries and violation status."
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
        />
      )}

      {clients && clients.length > 0 && <ClientsTable clients={clients} />}
    </div>
  );
}
