import { api } from "./client";
import { ClientSummary } from "@/types/client";

export function getClients() {
  return api.get<ClientSummary[]>("/api/v1/clients");
}

export function deleteClient(clientId: string) {
  return api.delete<{ client_id: string }>(`/api/v1/clients/${clientId}`);
}
