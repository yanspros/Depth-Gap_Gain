# Source provenance

This repository was prepared from a read-only canonical research checkout. To avoid exposing a private filesystem layout, source locations below are **repository-relative paths under the research checkout**, not machine-specific absolute paths. SHA256 values identify the audited source files. “Cleaned” means the public file was newly written from the audited algorithm/contract while removing paths, model loading, audio handling, and project orchestration.

| Public file or asset | Relative canonical source | Source SHA256 | Scientific role | Public treatment |
|---|---|---|---|---|
| `src/depth_gap_gain/dgg.py` | `10_distributed_language_capsules/scripts/run_c6_b_lao_depth_localization.py` | `1bb109639a2fe83e805e75db6a6922e8effd66fb6908ff0fca3b5010f6284a4c` | paired corpus-CER bootstrap, R16, strict Q16 | Cleaned implementation of frozen logic; no data/model paths copied. |
| `configs/paper/dgg_q16_contract.json` | `10_distributed_language_capsules/scripts/stage12_amharic_dgg_q16_runtime.py` | audited as a runtime adapter to the C6 engine | canonical decision mapping | Cleaned contract; negative DGG excluded from Late-16. |
| `src/depth_gap_gain/interventions.py` | `10_distributed_language_capsules/scripts/run_c8_a_intermediate_depth_discovery.py` | `c21fb7db1e1a7faa3506b3b57e9f163fc556557157af40b5278b5cf6d160e78c` | Base-shell suffix restoration | Cleaned declarative wiring audit. |
| `src/depth_gap_gain/adapters.py` | `10_distributed_language_capsules/runtime.py` | `194dd9a91610fab2c300df5e6e98994aa72b8ea1e1d614e2eafc1d2ec96af230` | canonical linear residual capsule | Cleaned `LinearCapsuleResidual` only; excludes the legacy SiLU capsule. |
| `configs/examples/residual_*.yaml` | `10_distributed_language_capsules/results/c20_lao_seed3_clean_recovery_v3_*/**/capsule_config.json` | formal configs record 7,400,988 / 7,409,184 counts | residual allocation identity | Public metadata recreated without packages/checkpoints. |
| `src/depth_gap_gain/lora.py` and LoRA configs | `10_distributed_language_capsules/scripts/c10_lora_depth_runtime.py` and `configs/c10_cross_peft_depth_generalization_protocol.json` | `14eea63a5c8f687605424601599b7b6c5764da4d53f3e6537a8333acaf5d1bac`; protocol `c11c4fedc5576af700ab7d9107c8150571c47333e86f312622b9d54c35f9dea8` | LoRA target/rank/budget contract | Cleaned metadata/helper; PEFT source is not copied. |
| `src/depth_gap_gain/diagnostics/*` | `10_distributed_language_capsules/scripts/run_c14_layerwise_adaptation_mechanism.py` | `24146d150e6a69dfd543ea9417225257f56b1a9ad2d17f2809b8240b1a810d83` | gradient, displacement, representation definitions | Cleaned numerical helpers; model-specific forward path excluded. |
| `results/paper/dgg/development_dgg_summary.json` | `10_distributed_language_capsules/results/c14_layerwise_adaptation_mechanism/diagnostic_baseline_comparison/results/dgg_development_evidence.json` | `c3223730c216dff3a06e89f77c0351999cece23df5510fc230fac6e0dd863008` | four-language development DGG summary | Sanitized numerical subset. |
| `results/paper/diagnostics/*` | `10_distributed_language_capsules/results/c14_layerwise_adaptation_mechanism/diagnostic_baseline_comparison/results/{language_decisions.csv,summary.json}` | CSV `c774eb320d5bab898f24d4ef1c21d5659596186792cf66af4b561a927367b235` | retrospective comparator results | Sanitized numerical subset. |
| `results/paper/functional_depth/*` | `10_distributed_language_capsules/results/c14_layerwise_adaptation_mechanism/analysis/functional_depth_landscape/{summary.json,bootstrap_results.json}` | summary `daed82f462fc439349ccb61f545012c76435e1b53f90bddf60e74274edebe6e6`; bootstrap `5ada96f5017127d320cf1ba582817b935ac48b5957ad84c570116ef2d45496e0` | post-hoc S12--A28 landscape | Sanitized aggregates only; no target/audio records. |
| `results/paper/functional_depth/holm_adjacent_comparisons.json` | `10_distributed_language_capsules/results/c14_layerwise_adaptation_mechanism/analysis/phase2_stat_cost_audit/multiple_comparison_correction.json` | `7d15da262ad0281031038d206838fd8f06b477ef6b0dbbe452b92503523580ea` | Holm sensitivity | Sanitized aggregate only. |
| `results/paper/robustness/retention_threshold_sensitivity.json` | `Paper/evidence/limitations/c18/sensitivity_analysis.json` | frozen C18 paper evidence asset | post-hoc R16 threshold sensitivity | Sanitized aggregate; does not amend tau_R. |
| `results/paper/dgg/table1_main_depth_results.csv` | `Paper/icasSP2027_camera_ready_package_v2/table1_main_results/table1_main_depth_results.csv` | `f8ba54076dad0745f5490a4d7e07258e05d48bc1828e85ff2d657056abafafd9` | Table 1 source rows | `source_path` and source SHA columns removed. |
| `results/paper/dgg/table2_selector_cross_peft.csv` | `Paper/icasSP2027_camera_ready_package_v2/table2_selector_cross_peft/table2_selector_cross_peft.csv` | `fa63b56431a60df8d485fab2046474f8b0edfe4973ca3ba98dfc8af6dc607920` | Table 2 source rows | `source_path` and source SHA columns removed. |

## Canonical identity audit

| Language | Base SHA256 | Canonical Full-SFT probe SHA256 | Probe identity | DGG development panel |
|---|---|---|---|---|
| Khmer | `730839316de585f4c8298ec0e1712efc10fb19c6fa4e36eb741cb8d51ebcf6aa` | `2be36009ff5add69b9a91a2afb92c2242433783df6c2bfa80f78ef549d4d39ef` | P0.2 checkpoint-500 | 100 in-domain target clusters (development) |
| Lao | `730839316de585f4c8298ec0e1712efc10fb19c6fa4e36eb741cb8d51ebcf6aa` | `e1c4c19f9ff8674c495158c09160500478420b14790fa38837872c7bb08f9165` | E8 / step 7312 | FLEURS development, 191 targets |
| Burmese | `730839316de585f4c8298ec0e1712efc10fb19c6fa4e36eb741cb8d51ebcf6aa` | `47238857230db6607b6828409e9446f60de87e13715ddb8daf1860fcd706d7ad` | E8 / step 12523 | FLEURS development, 384 targets |
| Finnish | `730839316de585f4c8298ec0e1712efc10fb19c6fa4e36eb741cb8d51ebcf6aa` | `0be8c1f8d7dcc22df6daf49efbe339d84ec6653c37d5be139507e62e073e4964` | E12 / step 16263 | FLEURS development, 415 targets |

All use `llm.layers.0...llm.layers.27`. The Full-SFT target is the native OmniVoice masked eight-codebook cross-entropy. The public package carries no model, token, prompt, or target record capable of re-running this computation.
