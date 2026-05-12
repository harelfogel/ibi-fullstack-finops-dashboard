"""Application constants - no magic numbers."""

from decimal import Decimal
from enum import StrEnum


# ── Upload constraints ──────────────────────────────────────────────
MAX_UPLOAD_SIZE_BYTES = 10_485_760  # 10 MB
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

# ── Pagination ──────────────────────────────────────────────────────
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200

# ── Violation thresholds ────────────────────────────────────────────
CONCENTRATION_RISK_THRESHOLD = Decimal("0.50")  # 50% of portfolio in single ISIN
DAY_TRADING_PAIR_THRESHOLD = 3  # buy+sell pairs in window
DAY_TRADING_WINDOW_HOURS = 24

# ── ISIN format ─────────────────────────────────────────────────────
ISIN_LENGTH = 12


# ── Enums ───────────────────────────────────────────────────────────
class TransactionAction(StrEnum):
    BUY = "buy"
    SELL = "sell"


class ViolationType(StrEnum):
    SHORT_SELLING = "short_selling"
    CONCENTRATION_RISK = "concentration_risk"
    DAY_TRADING = "day_trading"


class ViolationSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


class LLMProviderType(StrEnum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    MOCK = "mock"


class ErrorCode(StrEnum):
    # Upload errors
    UPLOAD_INVALID_FORMAT = "UPLOAD_INVALID_FORMAT"
    UPLOAD_TOO_LARGE = "UPLOAD_TOO_LARGE"
    UPLOAD_EMPTY_FILE = "UPLOAD_EMPTY_FILE"

    # Validation errors
    VALIDATION_FAILED = "VALIDATION_FAILED"
    VALIDATION_MISSING_COLUMNS = "VALIDATION_MISSING_COLUMNS"
    VALIDATION_DUPLICATE_TX_ID = "VALIDATION_DUPLICATE_TX_ID"
    VALIDATION_INVALID_ROW = "VALIDATION_INVALID_ROW"

    # Resource errors
    CLIENT_NOT_FOUND = "CLIENT_NOT_FOUND"
    TRANSACTION_NOT_FOUND = "TRANSACTION_NOT_FOUND"

    # Server errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    AI_SERVICE_ERROR = "AI_SERVICE_ERROR"


# ── CSV column mapping ──────────────────────────────────────────────
EXPECTED_CSV_COLUMNS = {
    "ClientId": "client_id",
    "TransactionId": "transaction_id",
    "ISIN": "isin",
    "Action": "action",
    "Quantity": "quantity",
    "Price": "price",
    "Timestamp": "timestamp",
}
