"""Deterministic statistical helpers used in paper-facing analyses."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np


def holm_adjust(p_values: Iterable[float]) -> list[float]:
    """Holm FWER adjustment in the input order."""
    values = [float(value) for value in p_values]
    if any(value < 0 or value > 1 or not np.isfinite(value) for value in values):
        raise ValueError("p-values must be finite and in [0, 1]")
    m = len(values)
    ordered = sorted(enumerate(values), key=lambda item: item[1])
    adjusted = [0.0] * m
    running = 0.0
    for rank, (index, value) in enumerate(ordered):
        running = max(running, min(1.0, (m - rank) * value))
        adjusted[index] = running
    return adjusted


def null_centered_one_sided_bootstrap_pvalue(
    paired_effects: np.ndarray, *, replicates: int = 100_000, seed: int = 20260831
) -> float:
    """One-sided null-centered bootstrap p-value for a mean paired effect.

    This helper is for the post-hoc functional-landscape sensitivity analysis.
    It does not replace the nominal paired-CI protocol used by DGG.
    """
    values = np.asarray(paired_effects, dtype=np.float64)
    if values.ndim != 1 or len(values) < 2 or not np.isfinite(values).all():
        raise ValueError("paired_effects must be a finite one-dimensional vector of length >= 2")
    observed = float(values.mean())
    centered = values - observed
    rng = np.random.default_rng(seed)
    extreme = 0
    total = 0
    for start in range(0, replicates, 10_000):
        count = min(10_000, replicates - start)
        index = rng.integers(0, len(values), size=(count, len(values)))
        draws = centered[index].mean(axis=1)
        extreme += int(np.count_nonzero(draws >= observed))
        total += count
    return float((extreme + 1) / (total + 1))
