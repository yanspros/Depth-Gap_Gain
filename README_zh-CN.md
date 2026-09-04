# Depth-Gap Gain（DGG）

DGG 是一个有界的功能性深度诊断：在 28 个 Transformer block 的 `Full-28` 与最后 16 个 block 的 `Late-16` 两种等预算 PEFT 分配之间，先用 Full-SFT probe 的开发集功能恢复差异作出冻结选择。

本仓库公开的是可复核的算法、轻量统计工具、配置模板和脱敏论文数值；不公开 OmniVoice 源码镜像、checkpoint、音频、prompt、ASR 转写或内部 manifest。

## 核心边界

- `S16/A28` 是诊断 hybrid：只替换 Transformer block，embedding 与 acoustic/output interface 继续来自 Base。
- `Late-16/Full-28` 是分别训练的等预算 PEFT allocation，不能与 hybrid 混为同一模型。
- Q16 的 leave-one-target-out 只检查点估计 gain 与 R16，不重做 bootstrap。
- 负 DGG 不是预定义的 Late-16 区域，只能输出 `No Prediction`。
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

详细科学定义见 [docs/METHOD.md](docs/METHOD.md)，数据与许可证边界见 [docs/DATA.md](docs/DATA.md) 与 [LICENSE_REVIEW.md](LICENSE_REVIEW.md)。
