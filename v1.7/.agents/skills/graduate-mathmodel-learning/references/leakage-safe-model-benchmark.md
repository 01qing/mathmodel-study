# Leakage-Safe Model Benchmark

## Goal

把“为什么选这个模型”变成可重复的比较证据，而不是口头判断。

本阶段覆盖：
- Q1 + Q2：特征选择策略与 pIC50 回归模型联合评测；
- Q3：5 个 ADMET 二分类任务分别评测。

Q4 暂不进入统一 benchmark，因为它首先需要解决：
- favorable 标签语义；
- 描述符可行域；
- 解释性区间/约束设计。

## Leakage boundary

### Q1/Q2
禁止：

`全体1974条数据选Top20 -> 再对这20个变量交叉验证`

这会让验证折的信息提前影响变量选择。

正确方式：

`imputation -> scaling -> selector -> model`

全部放进 Pipeline，并在每个 outer fold 内重新拟合 selector。

### Q3
每个 ADMET 标签分别处理。

标准化、特征选择、采样、阈值选择都只能使用训练折。
v0.9 默认不做 SMOTE，先建立 class-weight / 原始样本的无泄漏基准。

## Q1/Q2 candidates

Selectors:
- Mutual Information Top20
- ElasticNet embedded Top20
- ExtraTrees embedded Top20

Regressors:
- ElasticNet
- PLS
- RBF-SVR
- RandomForest
- HistGradientBoosting

Metrics:
- nested CV
- RMSE primary
- MAE secondary
- R² diagnostic
- outer-fold variance
- Top20 feature stability

## Q3 candidates

Feature modes:
- all cleaned descriptors
- Mutual Information TopK inside each fold

Classifiers:
- Logistic Regression
- RBF-SVC
- RandomForest
- HistGradientBoosting

Metrics:
- balanced accuracy
- MCC
- F1
- precision
- recall
- ROC-AUC
- PR-AUC
- Brier score
- accuracy only as descriptive metric

## Winner rule

不制造任意加权总分。

### Q2
1. lower RMSE
2. lower MAE
3. lower RMSE std
4. practical tie 时优先复杂度更低

### Q3
1. higher balanced accuracy
2. higher MCC
3. higher PR-AUC
4. lower balanced-accuracy std
5. practical tie 时优先复杂度更低

## Practical tie

所有候选使用同一组 outer folds。

对 winner 与 runner-up 做逐折差值：
如果均值差小于约 `1.96 * SE(diff)`，标记为 `practical_tie`。

这不是正式显著性检验，只是竞赛决策规则：
差异不足以稳定区分时，不强行宣称复杂模型更优。

## Q1 stability

每个 outer fold 保存 Top20：
- selection frequency
- average pairwise Jaccard

如果预测略好但 Top20 极不稳定，必须标记风险。

## Test isolation

50 个官方 test 化合物在 benchmark 中完全不使用。

只有 selector、model、hyperparameters、threshold policy 都冻结后，
才允许 fit full train 并预测 test。
