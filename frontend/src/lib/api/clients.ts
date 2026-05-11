import { api } from "./client";
import { ClientSummary } from "@/types/client";

export function getClients() {
  return api.get<ClientSummary[]>("/api/v1/clients");
}
