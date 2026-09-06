# DGG Decision-Rule Alignment Handoff for the Paper

状态：`READY_FOR_WINDOWS_CODEX_REVIEW`

范围：这是论文措辞/公式的最小修正清单；没有修改服务器上的论文文件或任何科研结果。

## 核心结论

公开实现已与冻结 C6/C8/C12 证据对齐。Late-16 **不要求** `DGG >= 0`；它要求的是 Full-SFT probe eligible、DGG paired CI 包含零、且 Q16 通过。冻结 C12 Lao E1/E2 实例本身就是负 DGG 点估计、CI 跨零、输出 `LAST` 的直接证据。

## A. Decision equation

请在 Windows/Overleaf 的方法部分核对 Late 分支。

若当前式子已经是下面的形式，则：`NO PAPER FORMULA CHANGE REQUIRED`。

```latex
\textsc{Late-16}\quad\text{if}\quad
c_L \le 0 \le c_U \ \land\ Q_{16}=1,
```

且它必须在 Full-SFT probe eligibility 的全局前提下解释：

```latex
\operatorname{CI}_{0.95}^{\rm low}
\!\left[\operatorname{CER}(\mathrm{Base})-
\operatorname{CER}(\mathrm{Full\mbox{-}SFT})\right] > 0.
```

**不要**在 Late 条件中加入 `DGG \ge 0` 或等价的点估计非负要求。

Full 分支保持：

```latex
\textsc{Full-28}\quad\text{if}\quad
\widehat{\mathrm{DGG}}>0 \ \land\ c_L>0.
```

其余情形为 `No Prediction`。为使 “not significant” 无歧义，建议补一句：DGG 的 CI 全在零以下也不是预定义的 Late-16 区域，仍为 `No Prediction`。

## B. 建议替换的文字

删除或改写任何类似以下的句子：

> A negative DGG lies outside the Late-16 region and returns No Prediction.

替换为：

> The Late-16 branch requires a DGG confidence interval that includes zero and a passing Q16 gate; it does not impose a sign constraint on the DGG point estimate. A confidence interval wholly below zero remains outside the pre-defined decision space and yields No Prediction.

## C. Full-SFT eligibility

确保方法、Fig. 1 decision text 与 caption 都明确：Base→Full-SFT development gain 的 paired 95% CI lower bound `>0` 是 **Full-28、Late-16 两个分支共同的全局前置条件**。它不能只被写作 Q16 内部检查。

## D. Abstract and Introduction

无需因本次 alignment 修改摘要或引言的科学主张；这是边界语义与实现一致性修复，不改变 Khmer/Lao/Burmese/Finnish 的冻结论文决定或任何实验结果。

## E. Frozen evidence to cite internally

- C8-B frozen v2 predictor: `DGG is not significant and Suffix-16 passes the frozen C6-B sufficiency Gate`.
- C12 frozen Lao E1: `DGG=-1.0653 pp`, 95% CI `[-4.6663,+2.3737]`, `probe_ready=true`, decision `LAST`.
- C12 frozen Lao E2: `DGG=-1.5180 pp`, 95% CI `[-5.2774,+2.1535]`, `probe_ready=true`, decision `LAST`.

These records establish the negative-point/zero-crossing boundary without touching a held-out result.
