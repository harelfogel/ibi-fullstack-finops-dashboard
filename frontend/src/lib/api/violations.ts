import { api } from "./client";
import { Violation } from "@/types/violation";

export function getViolations(clientId: string) {
  return api.get<Violation[]>(`/api/v1/clients/${clientId}/violations`);
}
