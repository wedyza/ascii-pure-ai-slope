from dataclasses import dataclass

VALID_FORMATS = {"video/mp4", "video/webm", "video/avi", "video/quicktime"}
MAX_SIZE_BYTES = 104_857_600  # 100MB
MAX_DURATION_SECONDS = 300  # 5 minutes


@dataclass
class ValidationResult:
    valid: bool
    error: str | None = None
    status_code: int = 400


def validate_format(content_type: str) -> ValidationResult:
    if content_type not in VALID_FORMATS:
        return ValidationResult(
            valid=False,
            error=f"Invalid file format. Supported: MP4, WebM, AVI, MOV",
        )
    return ValidationResult(valid=True)


def validate_size(size_bytes: int) -> ValidationResult:
    if size_bytes > MAX_SIZE_BYTES:
        return ValidationResult(
            valid=False,
            error=f"File too large. Maximum size: 100MB",
            status_code=413,
        )
    return ValidationResult(valid=True)


def validate_duration(duration_seconds: float) -> ValidationResult:
    if duration_seconds > MAX_DURATION_SECONDS:
        return ValidationResult(
            valid=False,
            error=f"Video duration exceeds 5-minute limit",
            status_code=422,
        )
    return ValidationResult(valid=True)


def validate_upload(content_type: str, size_bytes: int) -> ValidationResult:
    format_result = validate_format(content_type)
    if not format_result.valid:
        return format_result

    size_result = validate_size(size_bytes)
    if not size_result.valid:
        return size_result

    return ValidationResult(valid=True)
