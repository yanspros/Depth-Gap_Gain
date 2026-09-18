# Human evaluation: final Table 3

## Current authority

The final manuscript uses the audited **20-listener version**. Twenty adult
native listeners per language evaluated 40 test items for Burmese, Lao,
Finnish, and Amharic. Full-28 and Late-16 were compared separately within
Residual and LoRA, for pronunciation, naturalness, and speaker similarity.
Each setting/criterion contains 800 binary judgments; the 24 cells contain
19,200 judgments in total. No supplied trials were excluded. Systems were
hidden and presentation order was randomized.

The selected allocation is the first system in `comparison`: `Full vs Last`
for Burmese/Finnish and `Last vs Full` for Lao/Amharic. Here `Full` means
Full-28 and `Last` means Late-16. A choice of 1 favors the selected allocation;
0 favors its matched-budget alternative.

## Results and audit

- [Frozen full-precision aggregate](../results/paper/human_eval_table3.json)
- [Renderer and optional raw replay](../scripts/reproduce_human_eval_table3.py)
- Status: **HUMAN_EVAL_REPRO_AUDIT_PASS**.
- Raw panel: 19,200 rows; duplicate rows/keys, missing pairs, invalid IDs,
  invalid preferences, and script exclusions: all zero in the local audit.
- Table 3: 24/24 point estimates, 24/24 lower bounds, and 24/24 upper bounds
  match the manuscript at its displayed precision.
- All 24 point estimates favor the selected allocation. Eighteen CIs exclude
  50%; six include it. By criterion, lower bounds exceed 50% in 8/8
  pronunciation, 7/8 naturalness, and 3/8 speaker-similarity comparisons.

The audit establishes computational correspondence for the supplied records;
it is not independent verification of data collection or nominal interval
coverage. Public aggregate rendering alone is not a raw-data replay.

Release checks on 2026-09-18: the public aggregate command and authorized local
raw replay both passed, with 24/24 matches for each of point/lower/upper.
All 14 repository tests passed (10 existing tests and four human-release tests).
Existing Table 1/Table 2/Figure 2/functional-depth reproduction commands also
completed. No DGG/Q16 implementation, scientific threshold, or research result
was changed by this human-only release update.

## Actual estimator

For cell c, let y_cjk be the binary preference matrix, J=20 listeners,
K=40 items, N=JK=800, and p_c its raw mean. Estimate the variance components
from all C=24 cells with equal weights:

```text
E_L,c = sample_variance(mean_over_items(y_c), ddof=1) - p_c(1-p_c)/K
E_I,c = sample_variance(mean_over_listeners(y_c), ddof=1) - p_c(1-p_c)/J
tau_L^2 = max(0, mean_over_cells(E_L,c))
tau_I^2 = max(0, mean_over_cells(E_I,c))
Var(p_c) = p_c(1-p_c)/N + tau_L^2/J + tau_I^2/K
CI_c = clip(p_c +/- 1.959963984540054 * sqrt(Var(p_c)), 0, 1)
```

Non-positive components are truncated **after pooling**, not cell by cell.
Point estimates and CI endpoints are multiplied by 100. The script preserves
the authoritative NumPy/pandas calculation order and Python one-decimal
formatting, including its floating-point rounding behavior.

This is a deterministic, per-comparison **normal CI** with listener/item
variance components. It uses no resampling (bootstrap iterations = 0), no
random seed, and no multiplicity adjustment. Figure 2's Holm correction does
not apply to these intervals. `GLMM_NOT_AUDITABLE`: no current GLMM output
is used for Table 3, its CIs, or significance claims. An unaudited simulation
comment in the source script was not copied as a coverage claim.

## Reproduction

From the repository root, render and validate the public aggregate:

```bash
python scripts/reproduce_human_eval_table3.py
```

This standard-library-only path reports `HUMAN_EVAL_AGGREGATE_CHECK_PASS`
and writes Markdown, full-precision cells, and a check report under ignored
`artifacts/human_eval/`.

With separately authorized local trials, replay the actual estimator:

```bash
python -m pip install numpy pandas
python scripts/reproduce_human_eval_table3.py --trials /path/to/authorized_trials.csv
```

The replay checks 24 complete 20-by-40 cells, binary choices, duplicate keys,
within-language ID consistency, expected settings/criteria, and all displayed
point/CI values. It reports `HUMAN_EVAL_REPRO_AUDIT_PASS` only after a real
raw replay matches the frozen aggregate. The earlier local audit additionally
checked IDs against the private combined manifest. Outputs never include raw
records, listener IDs, item IDs, or the input path.

Required de-identified CSV schema:

| Field | Meaning |
|---|---|
| setting | Language followed by Residual or LoRA |
| comparison | Full vs Last, or Last vs Full; selected allocation first |
| criterion | pronunciation, naturalness, speaker_similarity |
| listener_id | Anonymous within-language listener code |
| item_id | Anonymous within-language test-item code |
| choice | Binary selected-allocation preference, 0 or 1 |

The archived audit environment was Python 3.14.7, NumPy 2.5.2, pandas 3.0.5;
these are provenance values, not a promise of bitwise floating-point identity
on all software versions. The checker requires absolute numeric agreement
within 1e-10 percentage points and exact one-decimal display agreement.

## Public/private boundary and provenance

Public files contain only aggregate results, estimator code, schema, and
source-file hashes. Raw trials, private manifests, recruitment/payment
records, contacts, internal paths, and contract metadata are not published.
**RAW_TRIAL_PUBLIC_RELEASE_PENDING_USER_CONFIRMATION**.

Source hashes are recorded by filename only in the aggregate's `provenance`.
The public estimator was adapted from the audited `ci_table4.py`; no raw
records, thresholds, or results were edited. The legacy filename `table4`
belongs to the research package; this release maps it to manuscript Table 3.

Author-confirmed ethics: evaluators were paid adults, informed and voluntary,
and could refuse or withdraw without penalty. The task was rating synthetic
speech, with coded IDs and no personally identifiable information collected.
The institution has no formal ethics review committee/IRB for this minimal-risk
evaluation. The authors report adherence to the principles of the Declaration
of Helsinki; no formal IRB approval or exemption is asserted.

## Historical protocol (not current evidence)

The old **10-listener / crossed-bootstrap** version is **SUPERSEDED**. It is
not used for the final manuscript, final Table 3, current replay, or current
statistical Gate. Earlier missing-human-evidence statements in the initial
release are superseded by the audited 20-listener release documented here.
