export interface Position {
  isin: string;
  current_quantity: number;
  average_cost: number;
  total_invested: number;
  realized_pnl: number;
  unrealized_pnl: number;
  market_value: number;
  last_calculated_at: string;
}

export interface Portfolio {
  client_id: string;
  positions: Position[];
  total_value: number;
  total_realized_pnl: number;
  total_unrealized_pnl: number;
}
