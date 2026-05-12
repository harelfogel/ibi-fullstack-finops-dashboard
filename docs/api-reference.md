# API Reference

Base URL: `http://localhost:8000`

All responses use the `ApiResponse<T>` envelope:

```json
{
  "success": true,
  "data": "<T>",
  "error": null,
  "pagination": null
}
```

Error responses:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

---

## Health

### GET /health

Returns service health status.

**Response:** `{"status": "ok"}`

---

## Transactions

### POST /api/v1/transactions/upload

Upload a CSV or XLSX file containing transactions.

**Request:** `multipart/form-data`
- `file`: CSV or XLSX file (max 10 MB)

**Required CSV columns:** ClientId, TransactionId, ISIN, Action, Quantity, Price, Timestamp

**Response:** `ApiResponse<UploadResult>`

```json
{
  "success": true,
  "data": {
    "batch_id": "uuid",
    "total_rows": 100,
    "valid_rows": 95,
    "error_rows": 5,
    "errors": [
      {
        "row": 3,
        "field": "quantity",
        "message": "Quantity must be positive"
      }
    ],
    "affected_clients": ["C001", "C002"]
  }
}
```

**Error codes:** `UPLOAD_INVALID_FORMAT`, `UPLOAD_TOO_LARGE`, `UPLOAD_EMPTY_FILE`, `VALIDATION_MISSING_COLUMNS`

### GET /api/v1/transactions

List transactions with optional filtering and pagination.

**Query parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | int | 1 | Page number |
| page_size | int | 50 | Items per page (max 200) |
| client_id | string | - | Filter by client |
| isin | string | - | Filter by ISIN |
| action | string | - | Filter by "buy" or "sell" |

**Response:** `ApiResponse<TransactionOut[]>` with `PaginationMeta`

---

## Clients

### GET /api/v1/clients

List all clients with portfolio summaries.

**Response:** `ApiResponse<ClientSummary[]>`

```json
{
  "success": true,
  "data": [
    {
      "client_id": "C001",
      "position_count": 3,
      "total_value": "15000.00",
      "total_realized_pnl": "500.00",
      "total_unrealized_pnl": "-200.00",
      "violation_count": 1
    }
  ]
}
```

### GET /api/v1/clients/{client_id}

Get detailed information for a specific client.

**Path parameters:** `client_id` (string)

**Response:** `ApiResponse<ClientDetail>`

**Error codes:** `CLIENT_NOT_FOUND` (404)

---

## Portfolio

### GET /api/v1/clients/{client_id}/portfolio

Get FIFO-calculated portfolio positions for a client.

**Path parameters:** `client_id` (string)

**Response:** `ApiResponse<PortfolioOut>`

```json
{
  "success": true,
  "data": {
    "client_id": "C001",
    "positions": [
      {
        "isin": "US0378331005",
        "current_quantity": "50.000000",
        "average_cost": "150.000000",
        "total_invested": "7500.000000",
        "realized_pnl": "200.000000",
        "unrealized_pnl": "-100.000000",
        "market_value": "7400.000000"
      }
    ],
    "total_value": "7400.000000",
    "total_realized_pnl": "200.000000",
    "total_unrealized_pnl": "-100.000000"
  }
}
```

**Error codes:** `CLIENT_NOT_FOUND` (404)

---

## Violations

### GET /api/v1/clients/{client_id}/violations

Get compliance violations detected for a client.

**Path parameters:** `client_id` (string)

**Response:** `ApiResponse<ViolationOut[]>`

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "client_id": "C001",
      "transaction_id": "TX005",
      "violation_type": "short_selling",
      "severity": "error",
      "message": "Short sell detected for ISIN US0378331005: sold 100 units but only 50 available",
      "details": {
        "isin": "US0378331005",
        "sold_quantity": 100,
        "available_quantity": 50
      },
      "detected_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Violation types and severities:**
| Type | Severity | Trigger |
|------|----------|---------|
| `short_selling` | error | Sell quantity exceeds available lots |
| `concentration_risk` | warning | Single ISIN > 50% of portfolio value |
| `day_trading` | warning | >= 3 buy+sell pairs for same ISIN within 24 hours |

**Error codes:** `CLIENT_NOT_FOUND` (404)

---

## Insights

### GET /api/v1/clients/{client_id}/insights

Get AI-generated portfolio insights for a client.

**Path parameters:** `client_id` (string)

**Response:** `ApiResponse<InsightOut>`

```json
{
  "success": true,
  "data": {
    "summary": "Client C001 has a moderately concentrated portfolio...",
    "recommendations": [
      "Consider diversifying holdings across more ISINs",
      "Review short selling activity for compliance",
      "Monitor day trading patterns"
    ],
    "risk_score": 6,
    "highlights": [
      "Portfolio concentrated in 2 ISINs",
      "1 active compliance violation",
      "Realized P&L positive at $500"
    ]
  }
}
```

**Notes:**
- Uses the configured LLM provider (Anthropic, OpenAI, or Mock)
- Falls back to Mock provider if LLM call fails
- `risk_score` range: 1-10
- Max 3 recommendations and 3 highlights

**Error codes:** `CLIENT_NOT_FOUND` (404), `AI_SERVICE_ERROR` (500)
