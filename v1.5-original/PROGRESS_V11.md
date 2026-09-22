# v1.1 Progress

## 本轮第一次真正使用“真实参赛代码”验证 Skill

公开仓库：
`Bureaux-Tao/modeling2021-D`

已审计：
- models/t1.py
- models/t2_rf.py
- models/t2_xgboost.py
- models/t3_svm.py
- models/t3_keras.py
- models/t4.py
- utils/pic50_to_ic50.py

## 真实代码发现

### Critical
1. Q2 官方 test 使用 `x_scaler.fit_transform(x_test)`，与训练空间不一致。
2. Q3 官方 test 使用 `pca_model.fit(pred_x).transform(pred_x)`，与训练 PCA 基底不一致。

### High
- 全数据 scaler 后再 CV
- 全数据监督式 Top20 后再进入下一问
- PCA 在 split 前 fit
- 同一 holdout 反复用于 PCA维数/kernel/C 选择
- `precision_score(y_pred, y_test)` / `recall_score(y_pred, y_test)` 参数顺序反了
- Keras PCA 同样在 split 前 fit
- Q4 `ADMET` 合成标签来源未找到，无法验证“至少3项较好”的实现

### Medium
- 多个超参数逐项单独扫，不能声称最终组合是全局最优
- 多处 `shuffle=False` 无明确顺序依据
- Q3 选模以 Accuracy 为核心

### 值得保留的做法
- Q4 不是无约束生成729维任意描述符，而是在观测到的高活性样本中提取范围，并用 IsolationForest 过滤；作为“数据支撑域”思路比任意连续空间优化更谨慎。
- pIC50→IC50 使用 `10^(9-pIC50)`，与 nM 单位一致。

## Skill 因此新增

- `external-modeling-code-audit.md`
- `2021_D_external_code_audit.json`
- `scan_ml_code_risks.py`
- `validate_external_code_audit.py`
- E13–E16 四个真实代码审查 eval

## 证据状态

- 代码文本审计：REAL / verified_from_code
- 公开 CSV 文件元数据：REAL
- 公开 CSV 数值完整落盘：当前环境仍未完成
- 真实数值复现：NOT_RUN
- 真实 benchmark：NOT_RUN

这一步验证了 Skill 的方向：
**优秀论文/代码必须同时审“思路”和“实现”，不能把能跑的代码当作正确代码。**
