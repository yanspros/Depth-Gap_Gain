"""Base-to-Full-SFT layerwise parameter-displacement comparator."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
import numpy as np


def relative_displacement(base: Mapping[str, Any], full_sft: Mapping[str, Any], *, epsilon: float = 1e-12) -> float:
    """Compute ``||theta_full-theta_base||_2 / (||theta_base||_2+eps)``.

    Input mappings must contain exactly matching floating-point block tensors;
    missing keys, unexpected keys, non-floating tensors, and shape drift fail
    closed rather than being silently ignored.
    """
    if set(base) != set(full_sft):
        raise ValueError("parameter-name mismatch")
    base_sq = 0.0
    delta_sq = 0.0
    for name in sorted(base):
        left = np.asarray(base[name])
        right = np.asarray(full_sft[name])
        if left.shape != right.shape or not np.issubdtype(left.dtype, np.floating) or not np.issubdtype(right.dtype, np.floating):
            raise ValueError(f"invalid matching parameter: {name}")
        base_sq += float(np.square(left, dtype=np.float64).sum())
        delta_sq += float(np.square(right.astype(np.float64) - left.astype(np.float64)).sum())
    return float(np.sqrt(delta_sq) / (np.sqrt(base_sq) + epsilon))
