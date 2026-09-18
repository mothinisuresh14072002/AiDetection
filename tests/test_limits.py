from aidetection.limits import MAX_UPLOAD_BYTES, validate_size


def test_exact_limit():
    validate_size(b"x" * MAX_UPLOAD_BYTES)


def test_over_limit():
    try:
        validate_size(b"x" * (MAX_UPLOAD_BYTES + 1))
    except ValueError as exc:
        assert "exceeds" in str(exc)
    else:
        raise AssertionError("expected oversize payload to be rejected")
