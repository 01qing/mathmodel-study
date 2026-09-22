# v0.7 Progress

## 本轮完成

1. 从题面本身提取 `2021_D_problem_facts.json`
2. 明确 IC50 / pIC50 的目标语义和单位核验规则
3. 发现并固定 Q4 的 ADMET favorable 标签方向问题
4. 将 CYP3A4 的“好坏方向”标记为题面歧义，要求显式约定/敏感性分析
5. 建立一份 `CONTAMINATED_REFERENCE_BASELINE`
6. 建立 100 分 Fresh Blind Eval rubric
7. 新增 `prepare_blind_eval.py`
8. 新增 `validate_blind_bundle.py`
9. 真正 Blind Eval 状态保持 `NOT_RUN`

## 为什么 Reference Baseline 不等于 Blind Eval

当前研发上下文已经看过两篇优秀论文的方法链。
即使后续分析只引用题面，也不能证明模型没有受到先验污染。

因此它只用于：
- 检查 Skill 的方向
- 建立评分金线
- 发现遗漏风险

不用于证明：
“Skill 独立做题已经通过”。

## 下一步

在新的隔离上下文运行：

`fresh blind eval -> score -> 与 reference baseline 比较`

如果 ≥80 且无 critical fail：
再进入论文逐问对照和代码复现。
