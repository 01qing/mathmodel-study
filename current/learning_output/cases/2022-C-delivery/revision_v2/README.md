# 2022-C 参考解答修订 v2

先读 REFERENCE_SOLUTION.md；实验分布见 MULTISEED_REPORT.md，学习来源与适用范围见 LEARNING_NOTES.md。

本轮从各组相同 v1 起点运行五个随机种子，每种子 60 次变异，共 1200 个新候选。20 个末轮方案通过独立检查，四组最终方案通过重放、9 项回归及 3,972,826 个工作簿单元格回读。返回道最小反例见 results/RETURN_AUDIT.json；本版仍禁用返回道。

## 复现

Python 3.12，求解和约束验证仅使用标准库。在本目录运行：

```sh
python code/replay_selected.py
python code/validate.py
python code/test_regressions.py
python code/audit_return.py
```

完整重跑本轮：`python code/multiseed.py`。起点在 seed_inputs/，不依赖 v1 目录。结果文件会覆盖；重新求解后需重新导出并回读 Excel。`code/solve.py` 保留为底层模型及旧搜索入口，直接执行该脚本会运行 v1 搜索流程，不能复现本轮五种子实验。

Excel 导出需要 Node.js 与 @oai/artifact-tool，依次运行 `node code/export_xlsx.mjs result11` 等四组。回读检查用 `python code/verify_xlsx.py`，需 openpyxl。绘图用 `python code/plot_results.py`，需 matplotlib。已经导出的四份 Excel 可以直接打开，无须安装这些工具。

## 证据与版本

results/ 包含所有种子候选轨迹及检查；deliverables/ 包含四份矩阵和图；INPUT_MANIFEST.json 保留官方来源身份，inputs.json 是实际计算字段。warmstarts/ 及 seed_inputs/ 保留历史初值来源。

v1 产物原样保留。本版是案例修订 v2，不是 MathModel-Core v2 或 v1.42。正式 Core 仍为 v1.41。追加算力、同题热启动得到的改善不构成等预算算法优越性、跨题泛化或获奖率提升证明。对不同到达节拍的稳健性也没有全面提高。
