# Paper-asset mapping

| Public asset | Role | Origin category | Scope |
|---|---|---|---|
| `results/paper/dgg/table1_main_depth_results.csv` | Table 1 numeric rows | camera-ready table package | mixed retrospective/prospective evidence; retain row labels |
| `results/paper/dgg/table2_selector_cross_peft.csv` | Table 2 selector/cross-PEFT rows | camera-ready table package | LoRA evidence includes Burmese confirmation and Lao directional support |
| `results/paper/dgg/development_dgg_summary.json` | Four-language development DGG comparator | development comparator archive | comparator only; Finnish outcome remains inconclusive |
| `results/paper/diagnostics/*` | gradient/displacement/representation comparison | retrospective diagnostic archive | retrospective only |
| `results/paper/robustness/retention_threshold_sensitivity.json` | R16 threshold sensitivity | post-hoc robustness archive | post-hoc; does not amend tau_R=0.5 |
| `results/paper/functional_depth/*` | S12--A28 landscape and Holm sensitivity | development-only functional-analysis archive | post-hoc development-only functional analysis |
| `results/paper/figures/figure2_suffix_restoration_profiles.json` | Figure 2 source data | Burmese/Lao development profile | post-hoc functional sanity check |

The final manuscript's human Table 3 is released separately as
`results/paper/human_eval_table3.json`; `scripts/reproduce_human_eval_table3.py`
renders its 24 cells. This supersedes the earlier missing-human-evidence status.
The legacy cross-PEFT `table2` filenames above are unchanged and are not the
final human Table 3. See [HUMAN_EVALUATION.md](HUMAN_EVALUATION.md) for the
20-listener authority and restricted raw-data replay.
