# Method contract

## Diagnostic hybrids

The audited backbone has 28 Transformer blocks (`llm.layers.0` through `llm.layers.27`). For suffix depth `K`, blocks `28-K...27` are copied from a selected Full-SFT probe checkpoint into a Base shell. Text/audio embeddings, acoustic heads, and non-Transformer interfaces remain from Base. No mixed checkpoint is saved.

`S16` restores blocks 12--27. `A28` restores all 28 Transformer blocks but is still a Base-shell diagnostic hybrid. The primary DGG is `CER(S16)-CER(A28)` on the same development targets, using target-level paired bootstrap and corpus CER (`sum edits / sum reference characters`).

## Bounded decision rule

The selector first requires **probe eligibility**: the paired bootstrap 95% CI lower bound for Base-to-Full-SFT development gain must be strictly positive. If it is not, the only output is `No Prediction`.

Given eligibility, `Full-28` requires a positive DGG point estimate and a strictly positive DGG CI lower bound. `Late-16` requires a DGG CI that includes zero and a passing Q16; it does not impose a point-estimate sign condition. A DGG CI wholly below zero is `No Prediction`. The full boundary specification is [CANONICAL_DECISION_CONTRACT.md](CANONICAL_DECISION_CONTRACT.md).

## Q16

On the complete development panel, Q16 requires the lower bound of each Base-to-Full-SFT and Base-to-S16 gain CI to be positive, plus `R16 >= 0.5`. The leave-one-target-out check operates on corpus point estimates only: every omitted-target panel must retain a positive S16 gain and `R16 >= 0.5`. It does not run an inner bootstrap.

## PEFT allocations

The diagnostic is intentionally separate from validation. Full-28 and Late-16 are trained PEFT allocations with matched budgets; they are not S16/A28 hybrids. The residual adapter uses the linear, no-activation capsule specified in `adapters.py`; the old SiLU capsule implementation is not the canonical residual baseline represented here.

## Retrospective comparators

Gradient score: `||g_l||_2/sqrt(N_l)` on frozen Base parameters, from the native masked eight-codebook supervised loss, with independent targets, microbatch one, evaluation mode, and no optimizer step.

Displacement: `||theta_full(l)-theta_base(l)||_2/(||theta_base(l)||_2+eps)`.

Representation drift: teacher-forced, aligned valid-token mean `1-cosine(h_base,h_full)`. These quantities measure different constructs and are reported only as retrospective comparators.

## Functional-depth sensitivity

The S12/S16/S20/S24/A28 grid is a post-hoc development-only functional-restoration sweep. For adjacent conditions, positive `CER(S_{k+4})-CER(S_k)` denotes a worsening after restoring more blocks. Nominal target-paired CIs describe each effect; a separate 16-hypothesis Holm-adjusted sensitivity uses one-sided null-centered bootstrap p-values. Neither changes DGG/Q16 or defines an arbitrary PEFT-depth selector.
