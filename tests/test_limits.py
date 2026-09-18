import pytest
from src.aidetection.limits import MAX_UPLOAD_BYTES, validate_size

def test_size_limit_accepts_boundary():
    validate_size(b"x" * MAX_UPLOAD_BYTES)

def test_size_limit_rejects_oversize():
    with pytest.raises(ValueError):
        validate_size(b"x" * (MAX_UPLOAD_BYTES + 1))
