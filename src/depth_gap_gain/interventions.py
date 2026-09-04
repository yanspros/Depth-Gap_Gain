"""Declarative checks for Base-shell suffix-restoration hybrids."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


TOTAL_BLOCKS = 28


@dataclass(frozen=True)
class RestorationSpec:
    name: str
    restored_blocks: tuple[int, ...]


def suffix_restoration(suffix_blocks: int) -> RestorationSpec:
    if suffix_blocks not in {12, 16, 20, 24, 28}:
        raise ValueError("supported suffix depths are 12, 16, 20, 24, and 28")
    return RestorationSpec(name="A28" if suffix_blocks == 28 else f"S{suffix_blocks}", restored_blocks=tuple(range(TOTAL_BLOCKS - suffix_blocks, TOTAL_BLOCKS)))


def expected_module_sources(suffix_blocks: int) -> dict[str, str]:
    """Return the frozen hybrid wiring contract.

    Embeddings and acoustic/output modules always remain on the Base path.
    Only ``llm.layers.0`` through ``llm.layers.27`` may be restored from the
    Full-SFT probe.  A28 is therefore a diagnostic hybrid, not full model.
    """
    spec = suffix_restoration(suffix_blocks)
    sources = {"llm.embed_tokens": "Base", "audio_embeddings": "Base", "audio_heads": "Base", "codebook_layer_offsets": "Base"}
    for layer in range(TOTAL_BLOCKS):
        sources[f"llm.layers.{layer}"] = "Full-SFT" if layer in spec.restored_blocks else "Base"
    return sources


def validate_wiring(observed: Mapping[str, str], suffix_blocks: int) -> None:
    expected = expected_module_sources(suffix_blocks)
    missing = sorted(set(expected) - set(observed))
    wrong = {name: {"expected": expected[name], "observed": observed[name]} for name in expected if name in observed and observed[name] != expected[name]}
    extras = sorted(set(observed) - set(expected))
    if missing or wrong or extras:
        raise ValueError(f"hybrid wiring mismatch: missing={missing}, wrong={wrong}, extras={extras}")
