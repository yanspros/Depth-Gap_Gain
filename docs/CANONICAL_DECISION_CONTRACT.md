# Canonical DGG/Q16 Decision Contract

This is the single public contract shared by the reference code, examples, tests, and paper-facing documentation. It was recovered from the frozen C6/C8/C12 scientific assets; the provenance and the public-alignment rationale are recorded in [CANONICAL_DECISION_CONTRACT_AUDIT.md](../CANONICAL_DECISION_CONTRACT_AUDIT.md).

## Scope and definitions

The decision uses development-only, same-target diagnostic hybrids:

- **S16:** Base Transformer blocks 0--11 plus selected Full-SFT probe blocks 12--27.
- **A28:** selected Full-SFT probe blocks 0--27.

Embeddings and acoustic/output interfaces remain on the Base path. S16/A28 are not trained PEFT candidates. The bounded PEFT allocations evaluated later are called Late-16 and Full-28.

`DGG = CER(S16) - CER(A28)`, computed with corpus CER and a target-level paired percentile bootstrap 95% confidence interval.

## A. Global probe eligibility

Before either depth branch can be selected, Base-to-Full-SFT gain must have a paired bootstrap 95% CI lower bound strictly greater than zero:

```text
PROBE_ELIGIBLE := CI_lower(CER(Base) - CER(Full-SFT)) > 0.
```

If this condition is false or unavailable, the selector returns `No Prediction`. It is a global precondition, not merely a Q16 sub-check.

## B. Full-28 branch

```text
PROBE_ELIGIBLE
and DGG point > 0
and CI_lower(DGG) > 0
    => Full-28
```

The lower-bound inequality is strict. A CI that merely touches zero does not qualify for Full-28.

## C. Q16 sufficiency gate

With `tau_R = 0.5` by default,

```text
R16 = (CER(Base) - CER(S16)) / (CER(Base) - CER(Full-SFT)).
```

On the complete development panel, Q16 requires all of:

1. `CI_lower(Base - Full-SFT) > 0`;
2. `CI_lower(Base - S16) > 0`;
3. `R16 >= tau_R`;
4. every leave-one-target-out panel has an S16 gain point estimate `> 0`;
5. every leave-one-target-out panel has `R16 >= tau_R`.

LOO evaluates corpus point estimates only and deliberately does **not** rerun a bootstrap. An unavailable, non-finite, or near-zero Full-SFT denominator makes R16 invalid and Q16 false.

## D. Late-16 branch

```text
PROBE_ELIGIBLE
and CI_lower(DGG) <= 0 <= CI_upper(DGG)
and Q16 = true
    => Late-16
```

The Late-16 branch does **not** require `DGG point >= 0`. A negative point estimate whose CI crosses zero can be Late-16 when Q16 passes. A DGG CI wholly below zero is not a pre-defined Late-16 region and returns `No Prediction`.

## E. No Prediction and boundary cases

All cases not covered by B or D return `No Prediction`.

| Boundary | Output |
| --- | --- |
| `DGG=-0.10`, CI `[-0.30,+0.10]`, Q16 passes, probe eligible | `Late-16` |
| `DGG=0`, CI includes zero, Q16 passes, probe eligible | `Late-16` |
| DGG CI touches zero, Q16 passes, probe eligible | `Late-16` |
| DGG CI wholly below zero | `No Prediction` |
| Probe ineligible with significantly positive DGG | `No Prediction` |
| Q16 false/unavailable, while DGG is not significantly positive | `No Prediction` |

This contract does not retrospectively alter any frozen scientific decision, threshold, evaluation panel, or PEFT result.
