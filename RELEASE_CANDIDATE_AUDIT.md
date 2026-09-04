# GitHub 首次发布前 Release Candidate 审计

## 问题、方法、最终结果

目标是在首次公开发布前，核验许可证、公开资产边界、可运行性、论文数值、敏感信息和远端 Git 状态。方法为 `DEBUG / READ_ONLY_RELEASE_AUDIT`：只读取科研源资产和远端状态；在开源目录内仅修正了错误的公开元数据与文档措辞。最终结果：`GITHUB_RELEASE_CANDIDATE_READY = FAIL`；未创建 commit，未 push。

## 一句话结论

代码健康、toy demo、Table 1/Fig.2 CPU 重建及敏感信息扫描均通过，但许可证版权主体未确认、远端 `main` 非空、且待公开的论文结果资产与本次指定的 comparator/PEFT 数值要求不一致。因此不能合法或安全地首次公开发布。

## 审计范围与已通过项目

- 公开仓库仅含新写的 DGG/Q16、hybrid wiring、残差/LoRA 预算、诊断辅助函数和脱敏数值资产；未 vendor OmniVoice、PEFT、Hugging Face、PyTorch 或 evaluator 源码。
- OmniVoice 和 Hugging Face PEFT 的上游 LICENSE 均为 Apache-2.0；它们在本仓库中仅作为外部依赖。没有发现被跟踪的 GPL/AGPL 源码。因此，第三方依赖本身不阻止将独立原创代码以 Apache-2.0 发布；但这不替代对本项目代码实际版权主体的确认。
- 在隔离 `/tmp` 虚拟环境中，`pip install -e '.[plot,test]'`、导入、`--help`、三种 toy case、`pytest -q`（10 passed）、`reproduce_table1.py`、`reproduce_fig2.py` 和 `reproduce_table2.py` 均通过。Table 2 对人类 P/N/S 正确输出不可用状态，未伪造人评数值。
- 当前 staged-equivalent 候选为 59 个文件；无文件超过 1 MiB，无音频、checkpoint、模型权重或大二进制候选。凭据与机器相关绝对路径扫描未发现真实泄露；普通算法术语不视为 secret。
- 所有四个公开 DGG 数值与本次审计输入一致：Khmer `+1.17 [ +0.35, +2.03 ]`、Lao `+0.88 [ -2.66, +4.43 ]` 且 `Q16=PASS`、Burmese `+2.19 [ +1.40, +2.98 ]`、Finnish `+1.34 [ +0.49, +2.23 ]`（均为百分点）。

## 阻塞项

### 1. 许可证版权主体未确认

仓库没有复制第三方源代码，因此 Apache-2.0 在技术许可证兼容性上可行；但没有可核验的声明说明新写的代码和数值整理资产由哪个个人或法人拥有、是否需要雇主/机构授权。Apache-2.0 必须由有权授予版权与专利许可的主体发布。故本轮没有创建 `LICENSE` 或 `NOTICE`。

为避免提交错误作者信息，本轮删除了占位 `CITATION.cff`，并从 `pyproject.toml` 移除了虚构作者及不适用的许可证 classifier。论文作者/出版物信息在确认后再补充。

### 2. 远端不是空仓库

`origin` 精确指向目标 URL，但 `origin/main` 已有提交 `be183cae90a56b18178f7735548e465ca7f96ff0`（GitHub 初始 README）。本地仓库尚无 commit，且工作树包含完整候选发布内容。根据本轮“远端变化不得覆盖、不得 force push”的约束，未执行 merge、commit 或 push。必须先由所有者决定如何将远端初始提交与本地候选安全合并。

### 3. 论文结果 authority mismatch

公开诊断资产的真实 outcome 口径为三个已解决 PEFT outcome（Khmer、Lao、Burmese）和一个 Finnish `INCONCLUSIVE`：Gradient `2/3`、Displacement `2/3`、Representation `1/3`、DGG `3/3`。它不能诚实地改写为四个已验证 outcome 的 `2/4`、`3/4`、`1/4`、`4/4`。

公开 Table 1 的 delta 定义为 `CER(Full) - CER(Late)`：Lao 为 `+5.0973 [ +2.3984, +7.8060 ]` pp，Burmese seed 1 为 `-1.4042 [ -1.9493, -0.8751 ]` pp（另有 seed 2），且表中没有 Finnish `+0.70` primary row。它与相反 delta 符号和 Finnish 数字的发布前核验要求不一致。数值资产未被修改；需先由论文 authority 确认应公开哪一套表格及统一 delta 方向。

### 4. GitHub-facing internal-label cleanup 尚未完成

已从 README/PAPER_MAPPING/OPEN_SOURCE_AUDIT 和初始整理报告移除内部阶段编号。审计仍发现 `results/paper/` 内的 `formal_gate`、`outcome_gate`、`lora_status`、source-path 字段及诊断摘要带有内部编号；这些字段必须在不改变任何数值的前提下做一次公开元数据脱敏，才可进入 staged 清单。`docs/SOURCE_PROVENANCE.md` 是允许保留相对历史来源名的唯一例外，且不含绝对路径。

## 人类 P/N/S 边界

人类 P/N/S 仍为 `UNAVAILABLE FOR PUBLIC REPRODUCTION`。公开脚本仅生成自动指标与明确的 unavailable 标记；没有从 manuscript、ASR、SIM-o 或 UTMOS 填补人评结果。

## 修改与未修改

本轮仅修改开源目录：删除无效的占位 `CITATION.cff`，清理 `pyproject.toml` 占位作者/许可证 classifier，并清理部分公开文档的内部流程名称。未修改任何原始科研资产、checkpoint、数值结果或原项目文件。

## 下一步

1. 由有权主体书面确认本仓库原创代码/数值整理资产的版权持有人及 Apache-2.0 授权；随后才能创建标准 `LICENSE`。
2. 由论文 authority 确认公开 comparator denominator、Finnish outcome 和 Table 1 delta 方向；只可选择/标注正确的现有冻结资产，不可重算或改写结果。
3. 所有者确认远端初始 README 的安全合并方案后，再进行一次新的 release-candidate 审计、首个 commit 和非强制 push。
