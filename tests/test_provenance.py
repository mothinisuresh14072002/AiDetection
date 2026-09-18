from aidetection.provenance import inspect_metadata


def test_empty():
    assert not inspect_metadata(b"").present


def test_marker():
    assert inspect_metadata(b"xx C2PA yy").present
