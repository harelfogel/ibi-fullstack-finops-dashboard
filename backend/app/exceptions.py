"""Custom exceptions and global error handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.constants import ErrorCode


class AppException(Exception):  # noqa: N818
    """Base application exception."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        status_code: int = 500,
        details: dict | None = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class UploadError(AppException):
    """Raised for file upload issues."""

    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.UPLOAD_INVALID_FORMAT):
        super().__init__(message=message, error_code=error_code, status_code=400)


class ValidationError(AppException):
    """Raised when data validation fails."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_FAILED,
            status_code=422,
            details=details,
        )


class NotFoundError(AppException):
    """Raised when a resource is not found."""

    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.CLIENT_NOT_FOUND):
        super().__init__(message=message, error_code=error_code, status_code=404)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    **({"details": exc.details} if exc.details else {}),
                },
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": ErrorCode.INTERNAL_ERROR,
                    "message": "An unexpected error occurred.",
                },
            },
        )
