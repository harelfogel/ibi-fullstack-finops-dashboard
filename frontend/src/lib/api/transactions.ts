import { api } from "./client";
import { UploadResult, Transaction } from "@/types/transaction";
import { ApiResponse } from "@/types/api";

export function uploadTransactions(file: File): Promise<ApiResponse<UploadResult>> {
  return api.upload<UploadResult>("/api/v1/transactions/upload", file);
}

export function getTransactions(params?: {
  page?: number;
  page_size?: number;
  client_id?: string;
}): Promise<ApiResponse<Transaction[]>> {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set("page", String(params.page));
  if (params?.page_size) searchParams.set("page_size", String(params.page_size));
  if (params?.client_id) searchParams.set("client_id", params.client_id);
  const qs = searchParams.toString();
  return api.get<Transaction[]>(`/api/v1/transactions${qs ? `?${qs}` : ""}`);
}
