export interface ClientSummary {
  client_id: string;
  position_count: number;
  total_value: number;
  total_realized_pnl: number;
  total_unrealized_pnl: number;
  violation_count: number;
  created_at: string;
}
