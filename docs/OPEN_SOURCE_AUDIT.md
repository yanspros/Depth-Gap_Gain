# Open-source audit

## Scientific contract

DGG is a development-only functional diagnostic between S16 and A28 Base-shell hybrids. Q16 uses the complete-panel bootstrap gains, R16 threshold `tau_R=0.5`, and point-estimate leave-one-target-out robustness. It predicts only Full-28, Late-16, or No Prediction; it does not inspect PEFT outcomes.

## Authority map

1. **DGG/Q16:** paired corpus-CER bootstrap, retention, leave-one-target-out, and strict decision logic are represented by the public implementation and contract file.
2. **Residual adapters:** the formal linear residual structure is `LinearCapsuleResidual`; it has no activation.
3. **LoRA:** target modules, rank/alpha, dropout, bias policy, and equal parameter counts are represented as public configuration metadata.
4. **Comparators:** gradient, displacement, and representation summaries are retrospective comparator evidence.
5. **Functional landscape:** S12/S16/S20/S24/A28 aggregates and the 16-comparison Holm sensitivity are post-hoc, development-only analyses.
6. **Paper tables:** Table 1/2 numeric rows retain evidence-role labels and do not flatten retrospective, prospective, test, and directional evidence into one claim.

## Important audit finding: legacy adapter discrepancy

An older implementation described a SiLU capsule. The formal residual allocation instead uses `rmsnorm-down-up-residual-scale-v1` with **no activation**. The public adapter implements only that linear baseline and explicitly excludes the legacy SiLU branch. This is a source-selection clarification; it does not modify research assets.

## Finnish and human-evaluation boundaries

The comparator summary marks the Finnish PEFT outcome `INCONCLUSIVE`; it is not counted as a resolved Full-28 validation.

Human-evaluation update (2026-09-18): the audited 20-listener release now
provides final Table 3 aggregates and the actual variance-component normal-CI
estimator. All 24 point estimates and interval endpoints match the manuscript.
Raw trials remain private; see [HUMAN_EVALUATION.md](HUMAN_EVALUATION.md).
This human-only update does not revise the historical comparator assets or
DGG/Q16 implementation.

## Redistribution boundary

Newly written public code is limited to analysis/wrapper code and compact numerical assets. The following are excluded: OmniVoice and PEFT source trees, evaluator implementations/weights, checkpoint weights, datasets/audio, prompts, speaker metadata, generated WAVs, token caches, ASR transcripts, private manifests, server logs, and all absolute environment paths.

## Result scope

The functional landscape and comparator analyses are retrospective/post-hoc supporting material. They do not change the DGG/Q16 decisions, redefine the Late-16 cutoff, select arbitrary depth, or make a prospective claim. The cost audit does not support an end-to-end GPU-hour saving claim; this repository does not claim one.
