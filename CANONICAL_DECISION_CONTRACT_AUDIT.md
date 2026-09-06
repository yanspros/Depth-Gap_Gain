# Canonical DGG/Q16 Decision-Contract Audit

运行类型：`DEBUG / READ_ONLY_AUDIT`

日期：2026-09-06
范围：仅审计科研源资产；未训练、未推理、未运行 ASR、未重算 CER/bootstrap，未修改科研项目资产。

## 一句话结论

公开仓库应采用 **CONTRACT_B**：当 Full-SFT probe 通过全局资格门、DGG 的 paired 95% CI 包含零、且 Q16 通过时，输出 `Late-16`，**不要求 DGG 点估计非负**。因此 `DGG=-0.10, CI=[-0.30,+0.10], Q16=1` 的正确输出是 `Late-16`。同时，Full-SFT probe eligibility 是所有深度分支的全局前置条件；旧公开实现可让它被 Full-28 分支绕过，属于实现不一致。

## 审计问题与证据

### A. Late-16 是否要求 `DGG point >= 0`？

结论：**否，采用 CONTRACT_B。**

| 证据层级 | 冻结来源 | 内容 |
| --- | --- | --- |
| 原始 Lao 严格 sufficiency | `10_distributed_language_capsules/scripts/run_c6_b_lao_depth_localization.py` (`1bb109…4a4c`)；`results/c6_b_lao_depth_localization/formal_gate.json` (`bb1d75…674d0`) | C6 规定 Base→Full-SFT 与 Base→Suffix-16 gain 的 bootstrap 下界均 `>0`、`R16>=0.5`、以及 LOO 点估计条件；它建立 Q16 的来源，但尚未定义通用 Full/Late selector。 |
| 冻结 v2 predictor | `results/c8_b_v2_predictor_contract/predictor_contract.json` (`92b77c…b4207`)；由 C12 protocol (`97ecb5…ad3a8`) 固定 | Full：显著正 DGG；Last：`DGG non-significant` 且 Suffix-16 严格 sufficiency 通过。文本没有 `point >= 0` 条件。 |
| 实际 Lao v2 执行 | `results/c12_early_dgg_probe_efficiency/c12_analysis.json` (`7b281c…3f02`)；正式报告 | Lao E1/step 915 的 DGG 为 `-1.0653 pp [-4.6663,+2.3737]`，`probe_ready=true`、严格 Q16 通过，冻结输出 `LAST`；E2 同样为 `-1.5180 pp [-5.2774,+2.1535]` 与 `LAST`。这直接排除“point 必须非负”。 |
| 后续冻结引用 | C19 Hebrew protocol (`a49a77…d7f8`) 与 C20 robustness artifacts | 均写为“显著正 DGG → Full；否则 DGG not significant 且 Q16=1 → Late”。C20 的严格重放明确保留 Lao `LAST_16`。 |

`run_c12_early_dgg_probe_efficiency.py` (`f4b231…ad38c`) 的历史实现为：`FULL` 当且仅当 `READY && point>0 && CI_lower>0`；否则 `LAST` 当 `READY && strict_Q16`。它实际覆盖上述负点估计、CI 跨零的 Lao 例子。该代码没有显式拒绝“CI 完全低于零”的 fallback；这在论文四语言冻结决策中没有发生，且不应被扩展为一个新的 Late 区域。

为把 v2 predictor 中的 **“DGG non-significant”** 固化为可审计、对称且 fail-closed 的公共语义，公开 contract 使用 `CI_lower <= 0 <= CI_upper`。这正是本审计题目给出的 CONTRACT_B，且不改变任一冻结论文决策。

### B. Full-SFT probe eligibility 是否是全局前置 Gate？

结论：**是。**

历史 C12 代码先计算 `ready = Base−Full-SFT point > 0 && CI_lower > 0`，然后只有 `ready` 才能进入 `FULL` 或 `LAST`。C6 严格 sufficiency 同样把 Base→Full-SFT gain CI lower bound `>0` 作为必要条件。后续 prospective protocols 将这一条件称为 Full-SFT learnability/probe eligibility。

公共实现修复采用不冗余的可观察定义：

```text
PROBE_ELIGIBLE := CI_lower(Base − Full-SFT) > 0
```

在有效 paired bootstrap 中该条件蕴含正的中心增益；历史 C12 额外显式检查正点估计，未产生不同的冻结论文结果。

旧公开 `analyze_dgg()` 仅在 Q16 内计算 Full-SFT gain，随后无条件调用 `decide_depth()`；因此在 `Full-SFT gain CI_lower <= 0` 但 DGG 显著为正时，旧代码会错误输出 `Full-28`。这是要修复的全局 Gate 绕过。

## 唯一公共 canonical contract

1. `PROBE_ELIGIBLE`：`CI_lower(Base−Full-SFT) > 0`；未通过即 `No Prediction`。
2. `DGG = CER(S16) − CER(A28)`，以相同 development targets 的 target-level paired bootstrap 计算。
3. `Full-28`：probe eligible，且 `DGG point > 0` 与 `DGG CI_lower > 0`。
4. `Late-16`：probe eligible，且 `DGG CI_lower <= 0 <= DGG CI_upper`，且严格 Q16 通过；不要求点估计非负。
5. 其他情形：`No Prediction`。特别是 DGG 的 CI 完全低于零时，不能被自动解释为 Late-16。

## Q16（不变）

完整 development panel 要求：

- Base→Full-SFT gain bootstrap 95% CI lower bound `>0`；
- Base→S16 gain bootstrap 95% CI lower bound `>0`；
- `R16=(CER_Base-CER_S16)/(CER_Base-CER_FullSFT) >= tau_R`，默认 `tau_R=0.5`；
- 每个 leave-one-target-out panel 的 S16 gain **点估计** `>0` 且 `R16>=tau_R`。

LOO 不重新运行 bootstrap。分母近零或 R16 不可定义时，Q16 为 false，因此结果 fail-closed 为 `No Prediction`。

## 边界表

| 情形 | Canonical output |
| --- | --- |
| `DGG point=-0.10`, `CI=[-0.30,+0.10]`, Q16=true，probe eligible | `Late-16` |
| `DGG point=0`, CI 包含零，Q16=true，probe eligible | `Late-16` |
| CI 恰触及零（例如 `[0,+0.10]`），Q16=true，probe eligible | `Late-16`；Full 使用严格的 `CI_lower>0` |
| DGG CI 全在负侧 | `No Prediction` |
| Full-SFT probe ineligible，即使 DGG 显著为正 | `No Prediction` |
| Q16 unavailable/false 或 R16 分母近零 | `No Prediction`（除非已满足 Full-28 的分支且 probe eligible） |

## 影响边界

- 本审计没有改动任何科研源代码、冻结 JSON、DGG/Q16 数值或四语言历史结论。
- 这是公开实现与论文/冻结协议的对齐修复；不是新实验，也不是对 C6/C12 的追溯性协议改写。
- 下游公共文件必须共同引用 `docs/CANONICAL_DECISION_CONTRACT.md`，其内容由本审计确定。

## 可交接运行报告

**问题/目标。** 公开代码此前把 `DGG point >= 0` 作为 Late-16 条件，并未在 Full-28 分支前执行 Full-SFT probe eligibility；目标是仅靠冻结资产确定唯一规则并消除这两处偏差。

**方法。** 只读核验 C6 的严格 sufficiency、C8-B 冻结 predictor、C12 实际 checkpoint 观察、C19 对 predictor 的复用，以及 C20 对 Lao 的重放审计；随后只修改公开仓库中的 contract、实现、测试和论文 handoff。

**最终结果。** Contract B 与全局 probe eligibility 都有冻结证据；C12 Lao E1/E2 是负点估计且 CI 跨零仍输出 `LAST` 的可复核反例。公开实现已改为 CI-based Late-16 分支并在失去 Full-SFT learnability 时 fail-closed。

**已解决。** 公开代码、配置、README、方法说明与边界测试统一为同一语义；四语公开 summary 仅被读取，未被修改。

**未解决。** 当前服务器没有可写的 Windows/Overleaf 论文工作树；`PAPER_ALIGNMENT_HANDOFF.md` 因而只提供最小文字/LaTex 修正，不直接修改论文。

**主要产物。** 本审计、`docs/CANONICAL_DECISION_CONTRACT.md`、`PAPER_ALIGNMENT_HANDOFF.md` 与相应单元测试均位于本开源仓库。下一步仅需由论文写作端应用 handoff 中的最小语义修正。
