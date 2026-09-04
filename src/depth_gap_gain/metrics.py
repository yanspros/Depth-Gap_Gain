"""Corpus-CER primitives used by DGG.

All paired statistics resample targets and recompute total edit distance over
total reference characters.  They do not average utterance-level CER values.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

import numpy as np


def _record_map(records: Iterable[Mapping[str, Any]], condition: str) -> dict[str, Mapping[str, Any]]:
    output: dict[str, Mapping[str, Any]] = {}
    for record in records:
        target_id = str(record["target_id"])
        if target_id in output:
            raise ValueError(f"duplicate target_id in {condition}: {target_id}")
        edits = float(record["edit_distance"])
        chars = float(record["reference_chars"])
        if edits < 0 or chars <= 0 or not np.isfinite([edits, chars]).all():
            raise ValueError(f"invalid CER counts in {condition}/{target_id}")
        output[target_id] = record
    if not output:
        raise ValueError(f"no records in {condition}")
    return output


def align_conditions(
    left: Iterable[Mapping[str, Any]], right: Iterable[Mapping[str, Any]], *, left_name: str, right_name: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Return aligned edit counts and reference characters, rejecting drift."""
    lmap, rmap = _record_map(left, left_name), _record_map(right, right_name)
    if set(lmap) != set(rmap):
        missing_left = sorted(set(rmap) - set(lmap))[:5]
        missing_right = sorted(set(lmap) - set(rmap))[:5]
        raise ValueError(f"target identity mismatch: only_{right_name}={missing_left}, only_{left_name}={missing_right}")
    target_ids = sorted(lmap)
    ledits = np.asarray([float(lmap[key]["edit_distance"]) for key in target_ids], dtype=np.float64)
    redits = np.asarray([float(rmap[key]["edit_distance"]) for key in target_ids], dtype=np.float64)
    lchars = np.asarray([float(lmap[key]["reference_chars"]) for key in target_ids], dtype=np.float64)
    rchars = np.asarray([float(rmap[key]["reference_chars"]) for key in target_ids], dtype=np.float64)
    if not np.array_equal(lchars, rchars):
        raise ValueError("reference character counts differ across paired conditions")
    return ledits, redits, lchars, target_ids


def corpus_cer(records: Iterable[Mapping[str, Any]]) -> float:
    mapping = _record_map(records, "records")
    edits = sum(float(row["edit_distance"]) for row in mapping.values())
    chars = sum(float(row["reference_chars"]) for row in mapping.values())
    return edits / chars


def paired_corpus_delta(
    left: Iterable[Mapping[str, Any]],
    right: Iterable[Mapping[str, Any]],
    *,
    left_name: str,
    right_name: str,
    replicates: int = 10_000,
    seed: int = 20260831,
) -> dict[str, Any]:
    """Estimate ``CER(left)-CER(right)`` with target-level paired bootstrap."""
    if replicates < 1:
        raise ValueError("replicates must be positive")
    ledits, redits, chars, target_ids = align_conditions(left, right, left_name=left_name, right_name=right_name)
    rng = np.random.default_rng(seed)
    draws: list[np.ndarray] = []
    # Chunked generation bounds memory while preserving one deterministic RNG stream.
    for start in range(0, replicates, 1_000):
        count = min(1_000, replicates - start)
        index = rng.integers(0, len(target_ids), size=(count, len(target_ids)))
        draws.append((ledits[index].sum(axis=1) - redits[index].sum(axis=1)) / chars[index].sum(axis=1))
    values = np.concatenate(draws)
    point = float((ledits.sum() - redits.sum()) / chars.sum())
    return {
        "definition": f"CER({left_name}) - CER({right_name})",
        "point": point,
        "ci95": [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))],
        "bootstrap": {"unit": "target_id", "replicates": int(replicates), "seed": int(seed), "ci": "two-sided percentile 95%"},
        "target_count": len(target_ids),
    }
