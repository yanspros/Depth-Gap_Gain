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


def evaluate_probe_eligibility(q16_or_gain: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate the global Full-SFT probe-eligibility precondition.

    This is intentionally separate from Q16's S16 sufficiency checks.
    The frozen selector cannot return either bounded-depth allocation when the
    Base-to-Full-SFT development gain does not have a strictly positive paired
    bootstrap lower bound (Base->Full-SFT 95% CI lower bound <= 0).
    """
    try:
        if "full_sft_gain" in q16_or_gain:
            lower = float(q16_or_gain["full_sft_gain"]["ci95"][0])
        elif "ci95" in q16_or_gain:
            lower = float(q16_or_gain["ci95"][0])
        else:
            return {
                "passed": False,
                "reason": "Full-SFT gain confidence interval is unavailable or invalid",
            }
    except (KeyError, IndexError, TypeError, ValueError):
        return {
            "passed": False,
            "reason": "Full-SFT gain confidence interval is unavailable or invalid",
        }
    if lower > 0:
        return {"passed": True, "reason": None}
    return {
        "passed": False,
        "reason": "Full-SFT gain lower bound <= 0",
    }


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
    finite_loo_r16 = loo_r16[np.isfinite(loo_r16)]
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
            "minimum_R16": float(np.min(finite_loo_r16)) if len(finite_loo_r16) else None,
        },
        "Q16": passed,
    }


def decide_depth(
    dgg: Mapping[str, Any],
    q16: Mapping[str, Any],
    *,
    probe_eligible: bool,
) -> str:
    """Return the bounded-depth decision according to Eq.(4) and final scientific contract.

    1. Global eligibility check:
       If probe_eligible is False (Base->Full-SFT 95% CI lower bound <= 0),
       return "No Prediction" regardless of DGG.
    2. Full-28 branch:
       probe_eligible is True and DGG point > 0 and CI_lower(DGG) > 0 -> "Full-28".
    3. Late-16 branch:
       probe_eligible is True and CI_lower(DGG) <= 0 <= CI_upper(DGG) and Q16 == True -> "Late-16".
       (Does not require DGG point >= 0).
    4. Fully negative DGG interval (CI_upper(DGG) < 0) or any other case -> "No Prediction".
    """
    if not probe_eligible:
        return "No Prediction"
    point = float(dgg["point"])
    lower, upper = (float(value) for value in dgg["ci95"])
    # Full-28: strictly positive DGG interval
    if point > 0 and lower > 0:
        return "Full-28"
    # Late-16: DGG interval contains 0 and Q16 passes (point estimate sign is unconstrained)
    if lower <= 0 <= upper and bool(q16.get("Q16", False)):
        return "Late-16"
    # Fully negative interval (upper < 0) or Q16 failure returns No Prediction
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
    probe_eligibility = evaluate_probe_eligibility(q16)
    return {
        "definition": "DGG = CER(S16) - CER(A28)",
        "conditions": {"Base": corpus_cer(base), "Full-SFT": corpus_cer(full_sft), "S16": corpus_cer(s16), "A28": corpus_cer(a28)},
        "DGG": dgg,
        "Q16": q16,
        "probe_eligibility": probe_eligibility,
        "decision": decide_depth(dgg, q16, probe_eligible=probe_eligibility["passed"]),
        "boundary": "Diagnostic S16/A28 hybrids are not the trained Late-16/Full-28 PEFT allocations.",
    }
