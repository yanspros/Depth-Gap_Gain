# Depth-Gap Gain（DGG）

DGG 是一个有界的功能性深度诊断：在 28 个 Transformer block 的 `Full-28` 与最后 16 个 block 的 `Late-16` 两种等预算 PEFT 分配之间，先用 Full-SFT probe 的开发集功能恢复差异作出冻结选择。

本仓库公开的是可复核的算法、轻量统计工具、配置模板和脱敏论文数值；不公开 OmniVoice 源码镜像、checkpoint、音频、prompt、ASR 转写或内部 manifest。

## 核心决策规则（对应论文 Eq.(4)）

1. **全局 Eligibility 准入**：`Base→Full-SFT` 配对 bootstrap 95% CI 下界必须 `>0`。若下界 `<=0`，无论 DGG 结果如何，均返回 `No Prediction`。
2. **Full-28**：通过准入，且 `DGG point > 0` 且 `DGG CI lower > 0` $\rightarrow$ `Full-28`。
3. **Late-16**：通过准入，且 DGG 95% CI 包含零（`CI lower <= 0 <= CI upper`），且 Q16 通过 $\rightarrow$ `Late-16`。**不要求** DGG 点估计非负。
4. **No Prediction**：DGG 区间完全在零以下（`CI upper < 0`）、跨零时 Q16 未通过、或未通过全局准入。
5. **Q16 门控**：完整开发集需 `Base→Full-SFT` 与 `Base→S16` 下界均 `>0` 且 `R16 >= 0.5`；每个 leave-one-target-out 只检查 S16 点估计增益 `>0` 与 `R16 >= 0.5`，不重做 bootstrap。
- `S16/A28` 是诊断 hybrid，`Late-16/Full-28` 是分别训练的等预算 PEFT allocation。
- S12/S20/S24 是开发集 post-hoc functional-restoration 分析，不是额外的 PEFT candidate，也不改变历史 DGG/Q16 决策。

## 快速运行（无需 GPU）

```bash
python -m pip install -e .
python scripts/run_dgg.py --input examples/toy_dgg/full28_case.json
pytest -q
python scripts/reproduce_table1.py
python scripts/reproduce_fig2.py
```

toy JSON 均为虚构 edit-count，仅验证算法逻辑，不能用于论文引用。

详细科学定义见 [docs/CANONICAL_DECISION_CONTRACT.md](docs/CANONICAL_DECISION_CONTRACT.md) 与 [docs/METHOD.md](docs/METHOD.md)，数据与许可证边界见 [docs/DATA.md](docs/DATA.md) 与 [LICENSE_REVIEW.md](LICENSE_REVIEW.md)。
