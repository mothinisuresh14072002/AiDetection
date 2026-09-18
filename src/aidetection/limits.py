MAX_UPLOAD_BYTES = 25 * 1024 * 1024

def validate_size(data: bytes) -> None:
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValueError(f"media exceeds {MAX_UPLOAD_BYTES} byte limit")
