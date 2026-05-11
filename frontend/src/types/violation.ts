export interface Violation {
  id: number;
  client_id: string;
  transaction_id: string | null;
  violation_type: "short_selling" | "concentration_risk" | "day_trading";
  severity: "error" | "warning";
  message: string;
  details: Record<string, unknown> | null;
  detected_at: string;
}
