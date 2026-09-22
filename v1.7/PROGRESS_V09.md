# v0.9 Progress

## 已完成

1. Q1 + Q2 联合 Leakage-Safe Pipeline
2. Q1 三类特征选择：
   - Mutual Information
   - ElasticNet embedded
   - ExtraTrees embedded
3. Q2 五类回归：
   - ElasticNet
   - PLS
   - RBF-SVR
   - RandomForest
   - HistGradientBoosting
4. Nested CV
5. 所有候选共享同一 outer folds
6. Q1 Top20 稳定性：
   - selection frequency
   - pairwise Jaccard
7. Q3 五标签独立模型竞争
8. Q3 多指标：
   - balanced accuracy
   - MCC
   - F1
   - precision / recall
   - ROC-AUC
   - PR-AUC
   - Brier
9. practical tie 规则
10. 推荐理由 / runner-up / switch condition
11. test 50 条完全隔离
12. benchmark contract + validator

## 最关键的边界

禁止：

`全数据选Top20 -> 再CV评价Q2`

正确：

`outer train -> preprocess -> selector -> inner tuning -> model -> outer validation`

因此 Q1 与 Q2 在性能验证时必须作为一个完整 Pipeline。

## 烟测

synthetic benchmark 已真正运行通过：
- Q2 产生推荐 Pipeline
- Q3 五个标签均产生独立推荐
- practical tie 分支实际触发
- decision explanation 实际生成
- `test_used = false`
- contract validator PASS

## 当前诚实状态

- Framework：PASS
- Synthetic smoke：PASS
- Real 2021 D benchmark：NOT_RUN
- Fresh Blind Eval：NOT_RUN

下一步：
真实数据一旦落盘后执行：
`data audit -> standard benchmark -> final fit -> paper comparison`
