"""Lightweight provenance/metadata helpers. Metadata alone never proves origin."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Provenance:
    present: bool
    signals: tuple[str, ...]


def inspect_metadata(data: bytes) -> Provenance:
    if not data:
        return Provenance(False, ("empty payload",))
    head = data[:4096].lower()
    signals = []
    if b"c2pa" in head or b"content credentials" in head:
        signals.append("content-credentials-marker-present")
    if b"photoshop" in head:
        signals.append("software-marker-present")
    return Provenance(bool(signals), tuple(signals) or ("no recognized provenance marker",))
