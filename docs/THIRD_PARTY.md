# Third-party components

| Dependency | Source | License observed locally | Redistribution here |
|---|---|---|---|
| OmniVoice | `https://github.com/k2-fsa/OmniVoice` | Apache-2.0 | No; install/clone upstream yourself. |
| Hugging Face PEFT | upstream `peft` package | dependency license must be reviewed by user environment | No; declared as optional dependency. |
| PyTorch | upstream package | upstream terms | No; optional dependency. |
| FLEURS | original dataset provider | provider-specific terms | No audio or metadata redistributed. |
| Omnilingual ASR / Qwen-ASR | original providers | provider-specific terms | No model, evaluator, or transcript redistributed. |

This project contains newly written integration and analysis code only. It does not vendor OmniVoice, PEFT, evaluator code, model weights, or datasets. Before release, verify the current licenses and versions of every installed dependency.
