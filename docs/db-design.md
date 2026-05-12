# Database Design

## ER Diagram

```
┌──────────────┐       ┌───────────────────┐
│   clients     │       │   transactions     │
├──────────────┤       ├───────────────────┤
│ id        PK │◀──┐   │ id            PK  │
│ client_id UQ │   ├───│ client_id     FK  │
│ created_at   │   │   │ transaction_id UQ │
│ updated_at   │   │   │ isin              │
└──────────────┘   │   │ action            │
                   │   │ quantity           │
                   │   │ price              │
                   │   │ timestamp          │
                   │   │ upload_batch_id    │
                   │   │ created_at         │
                   │   └───────────────────┘
                   │
┌──────────────────┤   ┌───────────────────┐
│ portfolio_       │   │   violations       │
│ positions        │   ├───────────────────┤
├──────────────────┤   │ id            PK  │
│ id           PK  │   │ client_id     FK ─┤
│ client_id    FK ─┘   │ transaction_id FK │
│ isin              │   │ violation_type    │
│ current_quantity  │   │ severity          │
│ average_cost      │   │ message           │
│ total_invested    │   │ details (JSON)    │
│ realized_pnl     │   │ detected_at       │
│ unrealized_pnl   │   └───────────────────┘
│ market_value      │
│ last_calculated_at│
└──────────────────┘
```

## Table Definitions

### clients

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| client_id | VARCHAR(50) | UNIQUE, NOT NULL |
| created_at | TIMESTAMP | DEFAULT now() |
| updated_at | TIMESTAMP | DEFAULT now(), ON UPDATE |

**Indexes:** `ix_clients_client_id` (unique)

### transactions

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| transaction_id | VARCHAR(50) | UNIQUE, NOT NULL |
| client_id | VARCHAR(50) | FK → clients.client_id, NOT NULL |
| isin | VARCHAR(12) | NOT NULL |
| action | VARCHAR(4) | CHECK IN ('buy', 'sell') |
| quantity | NUMERIC(18,6) | CHECK > 0 |
| price | NUMERIC(18,6) | CHECK > 0 |
| timestamp | TIMESTAMP(tz) | NOT NULL |
| upload_batch_id | UUID | NOT NULL |
| created_at | TIMESTAMP | DEFAULT now() |

**Indexes:**
- `ix_transactions_transaction_id` (unique)
- `ix_transactions_client_isin` (client_id, isin)
- `ix_transactions_client_timestamp` (client_id, timestamp)
- `ix_transactions_batch_id` (upload_batch_id)

### portfolio_positions

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| client_id | VARCHAR(50) | FK → clients.client_id, NOT NULL |
| isin | VARCHAR(12) | NOT NULL |
| current_quantity | NUMERIC(18,6) | |
| average_cost | NUMERIC(18,6) | |
| total_invested | NUMERIC(18,6) | |
| realized_pnl | NUMERIC(18,6) | |
| unrealized_pnl | NUMERIC(18,6) | |
| market_value | NUMERIC(18,6) | |
| last_calculated_at | TIMESTAMP | |

**Indexes:** `uq_positions_client_isin` (client_id, isin) UNIQUE

### violations

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| client_id | VARCHAR(50) | FK → clients.client_id, NOT NULL |
| transaction_id | VARCHAR(50) | FK → transactions.transaction_id, NULLABLE |
| violation_type | VARCHAR(30) | CHECK IN ('short_selling', 'concentration_risk', 'day_trading') |
| severity | VARCHAR(10) | CHECK IN ('error', 'warning') |
| message | TEXT | NOT NULL |
| details | JSON | NULLABLE |
| detected_at | TIMESTAMP | DEFAULT now() |

**Indexes:** `ix_violations_client_type` (client_id, violation_type)

## Design Decisions

- **Numeric(18,6)** for all financial values — avoids floating-point precision errors.
- **JSON over JSONB** for the details column — maintains SQLite compatibility for tests while PostgreSQL handles it natively in production.
- **CHECK constraints** at the DB level for action, quantity, price — defense in depth beyond application validation.
- **UUID batch tracking** (`upload_batch_id`) — enables tracing all transactions from a single upload.
- **Composite unique index** on positions (client_id + isin) — enforces one position record per client per instrument.
- **Nullable transaction_id** on violations — some violations (concentration risk) are portfolio-level, not tied to a single transaction.
- **Cascade recalculation** — portfolio positions and violations are fully recalculated from transaction history on each upload, ensuring consistency.
