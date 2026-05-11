"""CSV/XLSX file parser using pandas."""

import io
from pathlib import Path

import pandas as pd

from app.constants import ALLOWED_EXTENSIONS, EXPECTED_CSV_COLUMNS, MAX_UPLOAD_SIZE_BYTES, ErrorCode
from app.exceptions import UploadError


def parse_upload_file(filename: str, content: bytes) -> pd.DataFrame:
    """Parse an uploaded CSV or XLSX file into a normalized DataFrame.

    Args:
        filename: Original filename (used to detect format).
        content: Raw file bytes.

    Returns:
        DataFrame with columns renamed to snake_case.

    Raises:
        UploadError: If file format is invalid, too large, or missing columns.
    """
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise UploadError(
            f"Unsupported file format '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
            error_code=ErrorCode.UPLOAD_INVALID_FORMAT,
        )

    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise UploadError(
            f"File exceeds maximum size of {MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)}MB.",
            error_code=ErrorCode.UPLOAD_TOO_LARGE,
        )

    if len(content) == 0:
        raise UploadError("Uploaded file is empty.", error_code=ErrorCode.UPLOAD_EMPTY_FILE)

    try:
        if ext == ".csv":
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise UploadError(f"Failed to parse file: {e}") from e

    if df.empty:
        raise UploadError("File contains no data rows.", error_code=ErrorCode.UPLOAD_EMPTY_FILE)

    # Validate required columns
    missing = set(EXPECTED_CSV_COLUMNS.keys()) - set(df.columns)
    if missing:
        raise UploadError(
            f"Missing required columns: {', '.join(sorted(missing))}",
            error_code=ErrorCode.VALIDATION_MISSING_COLUMNS,
        )

    # Rename columns to snake_case
    df = df.rename(columns=EXPECTED_CSV_COLUMNS)

    return df
