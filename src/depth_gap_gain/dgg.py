"""Frozen Depth-Gap Gain (DGG) and Q16 decision logic."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np

from .metrics import align_conditions, corpus_cer, paired_corpus_delta


TAU_R_DEFAULT = 0.5


def _gain_records(base: list[Mapping[str, Any]], other: list[Mapping[str, Any]], other_name: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    base_edits, other_edits, chars, _ = align_conditions(base, other, left_name="Base", right_name=other_name)
    return base_edits, other_edits, chars


def evaluate_q16(
    base: list[Mapping[str, Any]],
    full_sft: list[Mapping[str, Any]],
    s16: list[Mapping[str, Any]],
    *,
    tau_r: float = TAU_R_DEFAULT,
    replicates: int = 10_000,
    seed: int = 20260831,
) -> dict[str, Any]:
    """Apply the canonical Q16 sufficiency gate.

    The full panel needs bootstrap lower bounds above zero for Base-to-Full
    and Base-to-S16 gains.  Each leave-one-target-out panel uses *point*
    gains and R16 only; it intentionally does not rerun a bootstrap.
    """
    if tau_r < 0:
        raise ValueError("tau_r must be non-negative")
    full_gain = paired_corpus_delta(base, full_sft, left_name="Base", right_name="Full-SFT", replicates=replicates, seed=seed)
    s16_gain = paired_corpus_delta(base, s16, left_name="Base", right_name="S16", replicates=replicates, seed=seed)
    base_e, full_e, chars = _gain_records(base, full_sft, "Full-SFT")
    base_s, s16_e, s16_chars = _gain_records(base, s16, "S16")
    if not np.array_equal(chars, s16_chars) or not np.array_equal(base_e, base_s):
        raise ValueError("Base records differ between Q16 comparisons")
    total_full = float((base_e.sum() - full_e.sum()) / chars.sum())
    total_s16 = float((base_e.sum() - s16_e.sum()) / chars.sum())
    r16 = None if abs(total_full) <= 1e-12 else float(total_s16 / total_full)
    loo_gain = (base_e.sum() - s16_e.sum() - (base_e - s16_e)) / (chars.sum() - chars)
    loo_full = (base_e.sum() - full_e.sum() - (base_e - full_e)) / (chars.sum() - chars)
    loo_r16 = np.divide(loo_gain, loo_full, out=np.full_like(loo_gain, np.nan), where=np.abs(loo_full) > 1e-12)
    loo_positive = bool(np.all(loo_gain > 0))
    loo_retained = bool(np.all(np.isfinite(loo_r16) & (loo_r16 >= tau_r)))
    passed = bool(
        full_gain["ci95"][0] > 0
        and s16_gain["ci95"][0] > 0
        and r16 is not None
        and r16 >= tau_r
        and loo_positive
        and loo_retained
    )
    return {
        "tau_R": float(tau_r),
        "full_sft_gain": full_gain,
        "s16_gain": s16_gain,
        "R16": r16,
        "leave_one_target_out": {
            "bootstrap_recomputed": False,
            "all_positive_s16_gain": loo_positive,
            "all_R16_at_least_tau_R": loo_retained,
            "minimum_s16_gain": float(np.min(loo_gain)),
            "minimum_R16": float(np.nanmin(loo_r16)),
        },
        "Q16": passed,
    }


def decide_depth(dgg: Mapping[str, Any], q16: Mapping[str, Any]) -> str:
    """Return the frozen bounded-depth decision without outcome information."""
    point = float(dgg["point"])
    lower, upper = (float(value) for value in dgg["ci95"])
    if point > 0 and lower > 0:
        return "Full-28"
    # A negative DGG is not part of the pre-defined Late-16 decision region.
    if point >= 0 and lower <= 0 <= upper and bool(q16["Q16"]):
        return "Late-16"
    return "No Prediction"


def analyze_dgg(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Analyze a JSON-compatible target-record payload.

    Required condition arrays are ``base``, ``full_sft``, ``s16``, and
    ``a28``.  A28 is the diagnostic hybrid; it is not a trained Full-28 PEFT
    arm.  Optional ``bootstrap`` and ``tau_R`` fields override defaults.
    """
    conditions = payload.get("conditions", payload)
    try:
        base = list(conditions["base"])
        full_sft = list(conditions["full_sft"])
        s16 = list(conditions["s16"])
        a28 = list(conditions["a28"])
    except KeyError as error:
        raise ValueError(f"missing condition: {error.args[0]}") from error
    bootstrap = payload.get("bootstrap", {})
    replicates = int(bootstrap.get("replicates", 10_000))
    seed = int(bootstrap.get("seed", 20260831))
    tau_r = float(payload.get("tau_R", TAU_R_DEFAULT))
    dgg = paired_corpus_delta(s16, a28, left_name="S16", right_name="A28", replicates=replicates, seed=seed)
    q16 = evaluate_q16(base, full_sft, s16, tau_r=tau_r, replicates=replicates, seed=seed)
    return {
        "definition": "DGG = CER(S16) - CER(A28)",
        "conditions": {"Base": corpus_cer(base), "Full-SFT": corpus_cer(full_sft), "S16": corpus_cer(s16), "A28": corpus_cer(a28)},
        "DGG": dgg,
        "Q16": q16,
        "decision": decide_depth(dgg, q16),
        "boundary": "Diagnostic S16/A28 hybrids are not the trained Late-16/Full-28 PEFT allocations.",
    }
