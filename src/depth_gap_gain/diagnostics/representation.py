"""Teacher-forced hidden-state drift comparator."""

from __future__ import annotations

import numpy as np


def cosine_drift(base_hidden: np.ndarray, full_hidden: np.ndarray, valid_mask: np.ndarray, *, epsilon: float = 1e-12) -> float:
    """Mean valid-token ``1-cosine`` drift for aligned hidden states."""
    base = np.asarray(base_hidden, dtype=np.float64)
    full = np.asarray(full_hidden, dtype=np.float64)
    mask = np.asarray(valid_mask, dtype=bool)
    if base.shape != full.shape or base.ndim != 2 or mask.shape != base.shape[:1] or not mask.any():
        raise ValueError("hidden states and valid mask must be aligned")
    left, right = base[mask], full[mask]
    cosine = (left * right).sum(axis=-1) / (np.linalg.norm(left, axis=-1) * np.linalg.norm(right, axis=-1) + epsilon)
    return float(np.mean(1.0 - cosine))
