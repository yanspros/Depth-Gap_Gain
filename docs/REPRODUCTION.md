# Reproduction levels

## Level 1 — CPU, no model

Install the core package and run the synthetic logic and paper-asset commands:

```bash
python -m pip install -e '.[plot,test]'
python scripts/run_dgg.py --input examples/toy_dgg/full28_case.json
pytest -q
python scripts/reproduce_table1.py
python scripts/reproduce_table2.py
python scripts/reproduce_fig2.py
```

This reproduces DGG/Q16 logic, deterministic statistics, curated Table 1/2 numeric assets, and the public development-only suffix-restoration figure. No checkpoint or audio is required.

### Human Table 3 (CPU only)

`python scripts/reproduce_human_eval_table3.py` renders and checks the public
20-listener aggregates using only the Python standard library. To replay the
estimator, install NumPy and pandas, then supply authorized local trials with
`--trials /path/to/authorized_trials.csv`. Raw records are not bundled. See
[HUMAN_EVALUATION.md](HUMAN_EVALUATION.md) for the method and output status.

## Level 2 — pretrained model plus public data

Obtain OmniVoice from its upstream repository, a compatible pretrained model, and legal public corpus access yourself. Point `DATA_ROOT`, `MODEL_ROOT`, and `OUTPUT_DIR` to your own locations. Use `configs/examples/dgg.yaml` to construct Base-shell S16/A28 hybrids, verify wiring, generate development audio, and evaluate with an independently licensed evaluator. The repository does not ship evaluator weights or audio data.

The gradient/displacement/representation comparators require an identical native supervised objective and aligned teacher-forced inputs; see `docs/METHOD.md`. They are retrospective analyses, not a substitute decision rule.

## Level 3 — GPU training

Reproducing the paper-style Full-SFT probe, matched Full-28/Late-16 residual adapters, and LoRA validation needs the exact public data version, model revision, compute environment, frozen development/test split, ASR route, and selection protocol. Templates are provided under `configs/examples/`, but no claim of one-command end-to-end reproducibility is made. Never use held-out test outcomes to choose LR, checkpoint, DGG parameters, or depth.

## Output interpretation

The public result assets are compact, frozen numerical summaries. They allow figure/table regeneration but cannot recreate TTS waveforms, ASR outputs, or the original sealed evaluation environment.
