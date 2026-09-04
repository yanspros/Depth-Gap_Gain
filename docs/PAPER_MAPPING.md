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

The current repository does not distribute Human P/N/S: the server-side canonical paper package records human listening evidence as `NOT_YET_RUN`. `scripts/reproduce_table2.py` therefore writes an explicit unavailable status.
