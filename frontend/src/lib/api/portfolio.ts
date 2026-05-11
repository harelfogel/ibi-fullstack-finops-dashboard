import { api } from "./client";
import { Portfolio } from "@/types/portfolio";

export function getPortfolio(clientId: string) {
  return api.get<Portfolio>(`/api/v1/clients/${clientId}/portfolio`);
}
