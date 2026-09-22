# External Modeling Code Audit Protocol

## Purpose

优秀论文和公开代码都不是“标准答案”。代码审计的目标是确认：

1. 数学任务是否被正确实现；
2. 训练、验证和测试边界是否干净；
3. 预处理是否只在训练数据上拟合；
4. 模型比较是否公平；
5. 评价指标是否与题目和数据分布匹配；
6. 最终预测是否使用与训练阶段一致的变换；
7. 代码结果是否足以支持论文主张。

## Audit order

### A. Data lineage
追踪每个对象：
- raw train
- raw test
- target
- feature matrix
- transformed train
- transformed validation
- transformed test

必须知道每一步数据从哪里来。

### B. Fit / transform boundary

高危：

```python
scaler.fit_transform(all_data)
train, val = train_test_split(...)
```

因为 scaler 已看到 validation。

正确：

```python
Pipeline([
    ("scaler", StandardScaler()),
    ("model", ...)
])
```

或只在训练折 `fit`，在 validation/test 上 `transform`。

### C. Test-transform consistency

严重错误：

```python
scaler.fit_transform(test)
pca.fit(test).transform(test)
```

若模型是在 train-fitted scaler/PCA 空间训练，test 必须使用同一个已拟合变换：

```python
scaler.transform(test)
pca.transform(test)
```

### D. Feature-selection leakage

高危：

```text
all train
→ supervised top-k
→ CV on selected features
```

如果 CV 用来声称泛化性能，selector 必须位于 CV 训练折内部。

### E. Holdout reuse

如果同一 holdout 被连续用于：
- 选 PCA 维数
- 选 kernel
- 选 C
- 选 threshold

它已经不是独立 test，而是 validation。

最终仍需要未参与选择的 outer validation/test。

### F. Metric semantics

检查：
- `y_true, y_pred` 顺序；
- 类别不平衡是否只看 Accuracy；
- 回归是否只看训练 R²；
- 概率进入下游决策时是否校准。

例如：

```python
precision_score(y_pred, y_true)
```

会改变指标语义；二分类中常表现为 precision/recall 对调。

### G. Hyperparameter strategy

逐参数单独调优：

```text
n_estimators
→ max_depth
→ max_features
→ min_samples_leaf
...
```

不是严格错误，但参数有交互时不能保证最终组合最优。

记录为 `methodological_risk`，不应写成“全局最优参数”。

### H. Order-dependent split

```python
train_test_split(..., shuffle=False)
```

只有在数据顺序有明确时间/组结构时才合理。

普通独立化合物样本若无顺序语义，应：
- 随机分层/随机 split；
- 或说明 group/time split 的理由。

### I. Q4 feasibility

检查代码是否真的实现题目条件：
- favorable ADMET 如何编码；
- CYP3A4 方向如何约定；
- “至少3项较好”是否明确；
- 描述符范围来自真实样本还是任意连续搜索；
- 是否把模型空间最优误称为真实可合成分子。

## Severity

- `critical`: 会使最终预测空间/数据边界错误，结果可能失效
- `high`: 泛化评价明显偏乐观或测试边界被污染
- `medium`: 方法选择/稳定性不足，影响可信度
- `low`: 可复现性、命名、工程质量问题

## Evidence status

- `verified_from_code`: 直接由源码确认
- `inferred_from_code`: 高可信推断，但缺少某个上游文件
- `unresolved`: 代码链缺失，不能下结论
