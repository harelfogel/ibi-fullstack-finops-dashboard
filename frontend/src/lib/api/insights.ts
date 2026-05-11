import { api } from "./client";
import { Insight } from "@/types/insight";

export function getInsights(clientId: string) {
  return api.get<Insight>(`/api/v1/clients/${clientId}/insights`);
}
