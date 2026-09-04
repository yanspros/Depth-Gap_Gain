"""Layerwise gradient-activity comparator."""

from __future__ import annotations

from collections.abc import Iterable
import numpy as np


def normalized_gradient_score(gradients: Iterable[np.ndarray]) -> dict[str, float]:
    """Return the frozen primary score ``||g_l||_2 / sqrt(N_l)``.

    Callers must obtain gradients from the frozen Base model with the native
    OmniVoice masked eight-codebook cross-entropy, one target at a time, with
    dropout disabled and no optimizer step.  This function only aggregates
    already-computed block gradients.
    """
    flat = [np.asarray(gradient, dtype=np.float64).ravel() for gradient in gradients]
    if not flat:
        raise ValueError("at least one gradient tensor is required")
    values = np.concatenate(flat)
    if not np.isfinite(values).all():
        raise ValueError("gradient contains non-finite values")
    raw = float(np.linalg.norm(values))
    return {"primary": raw / float(np.sqrt(values.size)), "raw_l2": raw, "parameter_count": int(values.size)}
