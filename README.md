# Depth-Gap Gain (DGG)

**Depth-Gap Gain is a bounded functional diagnostic for deciding whether a language adaptation should allocate a matched PEFT budget across all 28 Transformer blocks or only the final 16 blocks.**

This repository contains a cleaned reference implementation of the frozen DGG and Q16 logic, lightweight diagnostic comparators, public paper-result summaries, and CPU-only reproduction scripts. It deliberately does **not** redistribute OmniVoice, checkpoints, speech audio, prompts, ASR transcripts, or private manifests.

## What is DGG?

Starting from a Base checkpoint and a selected Full-SFT probe checkpoint, DGG constructs two **diagnostic hybrids**:

- **S16:** Base blocks 0--11 and Full-SFT probe blocks 12--27.
- **A28:** Full-SFT probe blocks 0--27.

Embeddings and acoustic/output interfaces remain on the Base path in both hybrids. With development-set corpus CER, `DGG = CER(S16) - CER(A28)`. Positive, statistically resolved DGG indicates additional lower-block functional benefit. DGG does not train either PEFT candidate.

### Do not conflate the two depth concepts

`S16/A28` are functional **diagnostic hybrids**. `Late-16/Full-28` are separately trained, matched-budget PEFT allocations. The former diagnoses a bounded depth choice; the latter validates that choice. S12/S20/S24 in the functional-depth analysis are also restoration hybrids, not extra PEFT arms.

## Decision rule

The canonical rule is implemented in `src/depth_gap_gain/dgg.py`.

- **Full-28:** DGG point estimate > 0 and its paired 95% CI lower bound > 0.
- **Late-16:** DGG point estimate >= 0, CI includes zero, and Q16 passes.
- **No Prediction:** all other cases. A negative DGG is never converted to a Late-16 prediction.

`Q16` requires, on the complete development panel: (i) a positive lower bound for Base-to-Full-SFT gain, (ii) a positive lower bound for Base-to-S16 gain, and (iii) `R16 >= tau_R`, where `R16=(CER_Base-CER_S16)/(CER_Base-CER_FullSFT)` and `tau_R=0.5` by default. For every leave-one-target-out panel, Q16 checks only the S16 point gain and R16; it intentionally does not recompute a bootstrap.

## Install

```bash
python -m pip install -e .
# Optional: pip install -e '.[plot,training,test]'
```

The core package requires only NumPy. Model integration additionally requires PyTorch, PEFT, an OmniVoice-compatible checkpoint, and legally obtained public data; see [docs/REPRODUCTION.md](docs/REPRODUCTION.md).

## CPU-only quick start

```bash
python scripts/run_dgg.py --input examples/toy_dgg/full28_case.json
python scripts/run_dgg.py --input examples/toy_dgg/late16_case.json
python scripts/run_dgg.py --input examples/toy_dgg/no_prediction_case.json
pytest -q
```

The toy records are synthetic logic tests, never paper evidence.

## Repository map

- `src/depth_gap_gain/`: DGG/Q16, corpus-CER bootstrap, hybrid wiring, residual/LoRA budget helpers, and retrospective comparator utilities.
- `configs/examples/`: path-neutral model-run templates.
- `results/paper/`: compact numerical assets sufficient to regenerate the public Table 1/Table 2 data and the development-only suffix-restoration Fig.2 without a GPU.
- `scripts/`: DGG runner and no-GPU table/figure reproduction commands.
- `docs/`: scientific contract, data and dependency boundaries, provenance, and release audit.

## PEFT allocations

The formal linear residual adapter is `RMSNorm -> Down -> Up -> scale -> residual`, with no activation. The matched allocations are Full-28 (`b=128`, 7,400,988 parameters) and Late-16 (`b=225`, 7,409,184 parameters).

The LoRA comparison targets Q/K/V/O attention and gate/up/down MLP projections. Full-28 uses `r=alpha=12`; Late-16 uses `r=alpha=21`; both canonical allocations have 7,569,408 trainable parameters in the audited backbone. This repository uses PEFT as a dependency rather than redistributing its source.

## Retrospective comparators

Gradient activity, Base-to-Full-SFT displacement, and hidden-state cosine drift are included as retrospective comparators. They quantify optimization activity, parameter movement, or representation drift—not functional contribution—and are not drop-in replacements for DGG.

## Functional depth analysis

`S12/S16/S20/S24/A28` profiles are post-hoc functional-restoration analyses on development data. They do not alter the DGG decision space or establish an arbitrary optimal PEFT depth. The adjacent-comparison Holm sensitivity is separate from the nominal DGG bootstrap protocol.

## Reproduce public results (no GPU)

```bash
python scripts/reproduce_table1.py
python scripts/reproduce_table2.py
python scripts/reproduce_fig2.py
python scripts/run_functional_depth_analysis.py
```

### Human listening evaluation (final manuscript Table 3)

Human listening evaluation used 20 adult native listeners per language and 40
test items for each of four languages: Burmese, Lao, Finnish, and Amharic.
Residual and LoRA Full-28/Late-16 comparisons were evaluated separately on
pronunciation, naturalness, and speaker similarity, yielding 800 judgments per
criterion per comparison (19,200 total). Table 3 reports raw preference
proportions with listener/item-aware variance-component normal confidence
intervals. The audited 20-listener release reproduces all 24 Table 3 cells.
All 24 point estimates favor the selected allocation; 18 intervals exclude
50% and six include it.

```bash
python scripts/reproduce_human_eval_table3.py
```

This command validates and renders the public aggregates; raw replay requires
authorized local trials and NumPy/pandas. Raw trials and manifests are not
published. See [Human evaluation](docs/HUMAN_EVALUATION.md) for the actual
estimator, audit provenance, schema, and replay command. The legacy
`reproduce_table2.py` command retains its existing cross-PEFT output and now
links to this audited human-evaluation release.

## Data, licensing, and limitations

See [docs/DATA.md](docs/DATA.md), [docs/THIRD_PARTY.md](docs/THIRD_PARTY.md), and [LICENSE_REVIEW.md](LICENSE_REVIEW.md). A release license has intentionally not been selected or applied yet. Before publishing, the repository owner must choose one for the newly authored code and confirm compatibility.

## Citation

Citation metadata will be added after the author list and associated manuscript metadata are confirmed. This release does not invent publication, DOI, or author information.
