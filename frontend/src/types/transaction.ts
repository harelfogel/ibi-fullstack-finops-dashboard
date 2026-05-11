export interface Transaction {
  transaction_id: string;
  client_id: string;
  isin: string;
  action: "buy" | "sell";
  quantity: number;
  price: number;
  timestamp: string;
  upload_batch_id: string;
}

export interface UploadError {
  row: number;
  field: string;
  message: string;
}

export interface UploadResult {
  batch_id: string;
  total_rows: number;
  valid_rows: number;
  error_rows: number;
  errors: UploadError[];
  affected_clients: string[];
}
