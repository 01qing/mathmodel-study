# 2021 D 真实公开代码审计

对象：`Bureaux-Tao/modeling2021-D`

本报告只审代码实现与数据边界，不把公开代码视为标准答案，也没有声称已经复现其数值结果。

## 总体判断

The repository is valuable as a real learning artifact, but its validation/test transformation chain contains issues serious enough that numerical results should not be treated as independently verified.

## 关键发现

### CRITICAL (2)

- **Q2-refit-scaler-on-official-test** 
  - 题目：Q2
  - 文件：`models/t2_rf.py`
  - 状态：`verified_from_code`
  - 证据：Official-test descriptors are transformed with x_scaler.fit_transform(x_test), not x_scaler.transform(x_test).
  - 影响：Test coordinates are mapped with test-specific min/max while the saved model was trained in train-specific coordinates; predictions are not in the same feature space.
  - Skill 规则：Never refit train-fitted transforms on test.

- **Q3-refit-pca-on-official-test** 
  - 题目：Q3
  - 文件：`models/t3_svm.py`
  - 状态：`verified_from_code`
  - 证据：x_pca_pred = pca_model.fit(pred_x).transform(pred_x) refits PCA on the test descriptors.
  - 影响：The SVM receives components in a different PCA basis from the one used for training; final predictions are not comparable in feature space.
  - Skill 规则：Use pca_model.transform(test) from the train-fitted PCA.

### HIGH (11)

- **Q1-full-data-scaling-before-cv** 
  - 题目：Q1
  - 文件：`models/t1.py`
  - 状态：`verified_from_code`
  - 证据：MinMaxScaler.fit_transform is applied to the full descriptor+target dataframe before GridSearchCV/cross_val_score.
  - 影响：CV folds inherit preprocessing parameters estimated using validation-fold rows; reported validation is not fully leakage-safe.
  - Skill 规则：Fit preprocessing inside each training fold.

- **Q1-full-data-supervised-top20** 
  - 题目：Q1/Q2
  - 文件：`models/t1.py`
  - 状态：`verified_from_code`
  - 证据：RandomForestRegressor is fit on all training rows and its feature_importances_ are used to print the top 20 descriptors.
  - 影响：If these Top20 are then reused in Q2 CV, Q2 validation has feature-selection leakage.
  - Skill 规则：When evaluating Q2, selector and regressor must be one nested-CV pipeline.

- **Q2-full-data-scaling-before-validation** 
  - 题目：Q2
  - 文件：`models/t2_rf.py`
  - 状态：`verified_from_code`
  - 证据：x_scaler.fit_transform(x_train) and y_scaler.fit_transform(y_train) occur before cross_val_score/GridSearchCV and before the later 80/20 holdout.
  - 影响：Validation rows affect preprocessing parameters.
  - Skill 规则：Fit scaler inside CV/holdout training partition only.

- **Q2-xgb-preprocessing-leakage** 
  - 题目：Q2
  - 文件：`models/t2_xgboost.py`
  - 状态：`verified_from_code`
  - 证据：MinMaxScaler is fit on the full X/y before the 80/20 split; subsequent tuning and holdout evaluation therefore use transforms estimated with holdout data.
  - 影响：Holdout estimate can be optimistic or otherwise contaminated.
  - Skill 规则：Split before fit or use a pipeline.

- **Q3-pca-fit-before-split** 
  - 题目：Q3
  - 文件：`models/t3_svm.py`
  - 状态：`verified_from_code`
  - 证据：PCA.fit(x_train).transform(x_train) occurs before train_test_split.
  - 影响：Holdout rows influence PCA basis.
  - Skill 规则：PCA must be fitted only on training folds.

- **Q3-reuse-same-holdout-for-selection** 
  - 题目：Q3
  - 文件：`models/t3_svm.py`
  - 状态：`verified_from_code`
  - 证据：The same 20% split is repeatedly evaluated while selecting n_components, kernel and C.
  - 影响：The nominal test split becomes a validation set; its best observed accuracy is selection-biased.
  - Skill 规则：Nested CV or separate train/validation/test.

- **Q3-precision-recall-arguments-reversed** 
  - 题目：Q3
  - 文件：`models/t3_svm.py`
  - 状态：`verified_from_code`
  - 证据：precision_score(y_pred, test_y) and recall_score(y_pred, test_y) pass prediction as y_true.
  - 影响：Reported precision/recall semantics are wrong; in binary classification they effectively swap roles relative to the intended arguments.
  - Skill 规则：Metric APIs must be checked as metric(y_true, y_pred).

- **Q3-test-duplication-workaround** 
  - 题目：Q3
  - 文件：`models/t3_svm.py`
  - 状态：`verified_from_code`
  - 证据：For a 'hERG/HOB - special' block, test rows are vertically duplicated before refitting PCA, then predictions are truncated back to half.
  - 影响：This does not repair the train/test PCA-basis mismatch and lacks a statistical justification in the audited code.
  - Skill 规则：Do not use data duplication to satisfy transform fitting requirements on test.

- **Q3-keras-pca-before-split** 
  - 题目：Q3
  - 文件：`models/t3_keras.py`
  - 状态：`verified_from_code`
  - 证据：For each candidate n_components, PCA is fit on all rows before the 80/20 split.
  - 影响：The holdout influences feature construction.
  - Skill 规则：Preprocessing belongs inside training partition.

- **Q3-keras-holdout-model-selection** 
  - 题目：Q3
  - 文件：`models/t3_keras.py`
  - 状态：`verified_from_code`
  - 证据：n_components from 20 to 49 are compared by model.evaluate on the same held-out 20%.
  - 影响：The held-out set is used for model selection and is no longer an unbiased test.
  - Skill 规则：Use validation/nested CV and reserve final test.

- **Q4-admet-composite-provenance-missing** 
  - 题目：Q4
  - 文件：`models/t4.py`
  - 状态：`unresolved`
  - 证据：t4.py consumes a prebuilt column named ADMET from data_all_train.csv, but the audited repository search did not reveal how that composite label was constructed.
  - 影响：Cannot verify whether favorable directions, CYP3A4 ambiguity, and the 'at least 3 favorable properties' rule were implemented correctly.
  - Skill 规则：Composite target derivation must be explicit and reproducible.

### MEDIUM (3)

- **Q2-sequential-hyperparameter-tuning** 
  - 题目：Q2
  - 文件：`models/t2_rf.py`
  - 状态：`verified_from_code`
  - 证据：n_estimators, max_depth, max_features, min_samples_leaf and min_samples_split are tuned in separate sequential sweeps.
  - 影响：Parameter interactions are not jointly optimized; the final combination is not established as globally best.
  - Skill 规则：Use a declared joint/random/Bayesian search or state the sequential-search limitation.

- **Q2-order-dependent-holdout** 
  - 题目：Q2
  - 文件：`models/t2_rf.py`
  - 状态：`verified_from_code`
  - 证据：train_test_split(..., shuffle=False) is used without an explicit order/group rationale in the audited file.
  - 影响：Performance can depend on arbitrary file order.
  - Skill 规则：Use random/group/time split according to data-generating structure and document why.

- **Q3-accuracy-primary** 
  - 题目：Q3
  - 文件：`models/t3_svm.py`
  - 状态：`verified_from_code`
  - 证据：Model-selection loops maximize accuracy_score.
  - 影响：Under label imbalance, model ranking can favor majority-class performance.
  - Skill 规则：Use balanced accuracy/MCC/PR-AUC and class-specific metrics.

### LOW (2)

- **Q4-observed-subset-range-strength** 【可取之处】
  - 题目：Q4
  - 文件：`models/t4.py`
  - 状态：`verified_from_code`
  - 证据：The code filters observed samples by pIC50 > 9, applies IsolationForest, then reports min/max ranges of selected descriptors.
  - 影响：Unlike unconstrained continuous optimization, the reported ranges are anchored to observed molecules; this is a useful feasibility-oriented idea, although the ADMET composite remains unresolved.
  - Skill 规则：Prefer observed/manifold-supported feasibility when direct molecular design is unavailable.

- **Q2-pic50-ic50-conversion** 【可取之处】
  - 题目：Q2
  - 文件：`utils/pic50_to_ic50.py`
  - 状态：`verified_from_code`
  - 证据：IC50 is computed as 10^(9-pIC50), consistent with IC50 in nM.
  - 影响：Target back-transformation is internally consistent with the stated nM convention.
  - Skill 规则：

## 最值得沉淀的错误模式

1. **预处理先看全数据，再做 CV**：即便 PCA 不看标签，验证折仍影响特征空间。
2. **test 重新 fit scaler/PCA**：这不是普通泄漏，而是训练空间与预测空间直接不一致。
3. **同一 holdout 被反复挑 PCA 维数、kernel、C**：它已经成为 validation，不能继续当独立 test。
4. **指标 API 能运行不代表语义正确**：`precision_score(y_pred, y_true)` 会改变 precision/recall 含义。
5. **代码缺链时保留 unresolved**：Q4 的复合 `ADMET` 标签来源未找到，不能猜它是否正确实现了“至少3项较好”。

## 也值得学习的地方

Q4 从实际观测到的高活性样本中提取描述符范围，并用 IsolationForest 过滤，这比在729维连续描述符空间任意生成“最优点”更接近数据支撑域思路。pIC50 到 IC50 的反变换也与 nM 单位一致。
