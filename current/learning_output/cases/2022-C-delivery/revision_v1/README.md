# 2022-C 参考解答修订 v1

这是 MathModel-Core v1.41 工作副本中的回顾性学习案例，不是新的 Core 发布版。先读 REFERENCE_SOLUTION.md，再读 LEARNING_NOTES.md。

## 文件

- deliverables/result11.xlsx、result12.xlsx、result21.xlsx、result22.xlsx：问题编号在前、附件编号在后。
- deliverables/result_analysis.png：基线、到达假设敏感性及搜索过程。
- code/：求解器、独立检查、回归、导出与绘图代码。
- inputs.json：本轮使用的官方附件字段快照；INPUT_MANIFEST.json 记录原始输入身份。
- warmstarts/：冻结 A 方案的动作记录，只用于提取初始车道分配，不宣称恢复原搜索代码。
- results/：搜索过程、结果矩阵、完整运动记录与各项核验。
- PACKAGE_MANIFEST.json：包内文件 SHA256。

## 运行

Python 3.12 下已执行验证。核心求解、快速重放和约束检查只用标准库。在本目录运行：

```sh
python code/replay_selected.py
python code/validate.py
python code/test_regressions.py
```

完整重跑搜索：`python code/solve.py --budget 40 --local 80`，会覆盖 results 中的求解结果。之后重新验证并导出工作簿，不能将旧工作簿误当新输出。

工作簿逐格读取检查需要 openpyxl：`python code/verify_xlsx.py`。重新绘图需要 matplotlib：`python code/plot_results.py`。重新导出需要 Node.js 和 @oai/artifact-tool：`node code/export_xlsx.mjs`；已交付的静态工作簿可直接使用，不需要此导出依赖。

## 验证范围

四组独立运动与约束检查通过，9 项回归通过，四组已选策略重放通过，4,087,028 个工作簿单元格与保存矩阵完全一致。检查不包含未使用的返回道；一个固定搜索种子、同题调参，不证明全局最优或跨题泛化。论文学习仅覆盖指定章节，不提高全文复现等级。包中不附优秀论文全文。
