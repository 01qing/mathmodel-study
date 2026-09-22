# 2022-C 参考解答修订 v3

先读 REFERENCE_SOLUTION.md。本轮实现并验证返回道，比较两种路线各 24 次候选评估；问题二附件 1 最终返回一次，其他三组不返回。案例 v3 不是 Core 新发布版本，正式基线仍为 v1.41。

## 复现入口

Python 3.12，核心求解和独立检查只使用标准库。在本目录运行：

```sh
python code/replay_returns.py
python code/test_returns.py
```

完整重跑本轮对照：`python code/compare_returns.py`。固定起点在 seed_inputs/，官方字段快照在 inputs.json。重新计算会覆盖 results 下的结果，之后必须重新导出并回读 Excel。

四个文件 result11.xlsx、result12.xlsx、result21.xlsx、result22.xlsx 中，第一位是问题编号，第二位是附件编号。可直接打开。导出用 `node code/export_xlsx.mjs result11` 等，需要 @oai/artifact-tool；回读用 `python code/verify_xlsx.py`，需 openpyxl；绘图用 `python code/plot_results.py`，需 matplotlib。

## 证据与边界

results/RETURN_COMPARISON.json 记录两路线比较；各 *_search.json 保留每个候选、返回设置和得分；*_best.json 保存两路线最终方案。新成为最优的候选必须通过独立检查才接受，其余候选不声称全部通过独立检查。

SELECTED_RETURN_REPLAY.json 是最终四组的最新独立重放证据；RETURN_REGRESSIONS.json、RETURN_STRESS.json 是回归和压力样例；XLSX_VALIDATION.json 记录逐格回读；PACKAGE_MANIFEST.json 记录文件哈希。

code/return_solver.py 为含返回的求解器，validate_returns.py 为独立检查器；solve.py、historical_base.py、validate.py 为继承的底层模块，应使用上面的新入口运行。旧阶段其他脚本不包含在本复现包中。

同候选次数不等于同墙钟耗时，搜索范围有限且同题已暴露。本次没有最优性、跨题泛化或获奖率证据，也没有新增全文论文学习。返回路线的正确性证据限于声明的时间语义和已测案例。
