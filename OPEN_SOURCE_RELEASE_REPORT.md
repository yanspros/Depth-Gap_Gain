# 开源发布整理报告

## 问题 / 目标 / 最终结果

目标是从只读的 DGG 多语种 TTS 科研项目中抽取论文真正需要公开的代码、配置和最小结果资产，建立一个不含模型、音频、私有 manifest 或内部路径的独立 GitHub 仓库。初始整理完成了核心 DGG/Q16、hybrid wiring、残差/LoRA 预算、三种 retrospective comparator、functional-depth/Holm 结果资产、CPU toy demo、测试和无 GPU 表图复现。该初始整理当时为 `OPEN_SOURCE_RELEASE_READY = PARTIAL`；当前首次发布资格以 [RELEASE_CANDIDATE_AUDIT.md](RELEASE_CANDIDATE_AUDIT.md) 为准。

## 一句话结论

仓库可在无 GPU 条件下复现 DGG/Q16 逻辑、Table 1/2 数值资产和 development-only Fig.2；首次 push 仍须通过独立的 Release Candidate 审计，本初始整理没有 push。

## 为什么做

原科研工作区包含 checkpoint、音频、评测缓存、内部 manifest 和阶段化运行器，不能整体公开。整理工作必须保留论文科学定义与结果 provenance，同时移除内部环境耦合和不可再分发资产。

## 做了什么

1. 只读审计 DGG/Q16、残差 adapter、LoRA、三种诊断 comparator、functional-depth/Holm、论文 Table 1/2 和 human-evidence authority。
2. 从冻结数学/结构定义编写独立的公开实现；未复制 OmniVoice、PEFT 或任何第三方源树。
3. 以路径参数化提取脚本生成脱敏的数值结果；没有复制 target-level 音频、ASR 转写、checkpoint、prompt 或内部 manifest。
4. 建立英文/中文 README、方法、数据、第三方、论文映射、来源 provenance 和许可证审计文档。
5. 初始化本地 Git `main`，设置正确 `origin`，但未执行 `git push`。

## 科学与工程核验

- DGG/Q16：三个 synthetic case 分别输出 `Full-28`、`Late-16` 和 `No Prediction`；负 DGG 不进入 Late-16 区域。
- 单元测试：临时、隔离的 `/tmp` pytest 依赖下 `10 passed`。
- 无 GPU 复现：`reproduce_table1.py`、`reproduce_table2.py`、`reproduce_fig2.py`、`run_functional_depth_analysis.py` 均完成并写入 `artifacts/`（该目录被 `.gitignore` 排除）。
- Figure 2：PDF、PNG、SVG 均由公开数值资产生成；PNG 已目视检查，文字、误差条和零参考线清晰。系统没有 Poppler，因此未进行 PDF raster replay；PDF 本身由 Matplotlib 矢量后端生成。
- 完整性：11 个跟踪候选 JSON 可解析；全部公开 CLI 的 `--help` 通过；没有大于 20 MiB 的待跟踪文件。
- 安全扫描：没有内部存储路径、用户名目录、凭据字段或机器主机标识泄露。`private` 和 `token` 命中仅为正常算法/数据边界用语，已人工确认非泄露。

## 已解决与未解决

已解决：核心算法可运行、Q16 leave-one-target-out 不重做 bootstrap、Full/Late 预算可计算、公开结果可无 GPU 重建。2026-09-18 human-only 更新已加入真实 20-listener Table 3 汇总与估计器，不使用自动指标替代人评。

未解决：

1. 发布 LICENSE 尚未由仓库所有者选择，故未创建顶层 `LICENSE`。
2. 已审计到 OmniVoice 为 Apache-2.0，但本仓库不重分发其代码；未来新增任何复制内容前仍需重新做兼容性核验。
3. 人评历史缺项已由 2026-09-18 的 20-listener release 闭合，见 [Human evaluation](docs/HUMAN_EVALUATION.md)。公开汇总与估计器，原始 trial 和 manifest 不公开；旧 10-listener 协议仅作 superseded 历史记录。

## 修改情况与主要产物

所有新增文件仅位于本开源目录。核心入口：

- `src/depth_gap_gain/dgg.py`
- `src/depth_gap_gain/adapters.py`
- `src/depth_gap_gain/lora.py`
- `docs/SOURCE_PROVENANCE.md`
- `docs/OPEN_SOURCE_AUDIT.md`
- `results/paper/`
- `scripts/reproduce_table1.py`
- `scripts/reproduce_table2.py`
- `scripts/reproduce_fig2.py`

## 当前结论与下一步

初始整理为 `OPEN_SOURCE_RELEASE_READY = PARTIAL`。首次公开发布前的当前状态、阻塞项和后续决策以 `RELEASE_CANDIDATE_AUDIT.md` 为准；本文件不替代 Release Candidate Gate。
