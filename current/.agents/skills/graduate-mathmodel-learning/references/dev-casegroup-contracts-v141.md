# v1.41 — 2024-D Dev case-group generic contracts

来源：2024-D 的 frozen independent solution 与 S013–S016 Dev 对照。这里只保留跨题可迁移的决策/审计门禁；论文特定参数、阈值、地名、未来风险数值和模型排行榜不进入普通 Train retrieval。

## 1. 统计对象与结果同源

- 每个统计量显式登记 `entity/support × time_support × operator × unit × denominator × missing_policy × weight`。
- `sum / mean / SD / variance / rate / fraction` 不能靠字段名互换；表、图、摘要和代码必须追到同一 Result Registry 记录。
- mean±SD 只有在明示估计对象时才能解释为不确定性；SD 本身不是均值置信区间。

## 2. 重采样、基率与目标总体

- 欠采样/过采样/类别平衡仅在训练折内进行；开发/测试保持部署目标总体。
- 抽样后类别比例不是原总体风险。若需要总体概率，必须恢复抽样机制/权重并校准。
- 稀有事件同时报告原总体暴露分母、少数类 recall/precision/PR 或适合任务的校准指标；总体 accuracy 不能替代少数类能力。

## 3. 标签谱系与预测可用性

- 对监督/风险任务保存 `label_source`, `label_definition`, `forecast_origin`, `available_at`, `prediction_scope`。
- 目标或由目标直接构造的特征不得进入部署预测器；以自构指数阈值生成的伪标签只能证明“重建该规则”，不能证明真实灾害/损失预测。
- 历史空间聚类/风险命名没有时间状态，不能直接挂未来年份当未来演化。

## 4. 评价机制必须分开登记

- `fitted`, `OOB`, `cross_validation`, `holdout`, `rolling_time`, `spatial_block` 属于不同 evaluator；禁止混排。
- 硬类别 ROC/AUC只对应有限工作点，不替代连续 score 的全阈值排序证据。
- 混淆矩阵、回归指标、SHAP/解释输出必须有 `run_id / split_id / target_id / entity_id` 才允许拼接或比较。

## 5. 未来预测与回测

- 未来地图、11个未来年份、情景数量都不是独立验证次数。
- 预测模型先与 persistence / climatology / simple trend 在历史滚动或预定 pseudo-future 窗口比较；未来驱动必须在 forecast origin 可获得，或明确标记为外部情景/假设。
- 无真实 future/disaster truth 时收窄结论为条件危险性、相对排序或情景敏感性，不制造已校准概率。

## 6. 组成、类别与流量可识别性

- 组成份额声明完整类别还是 partial composition；保留 other/background，检查边界和总量。
- 两期边际份额/面积的差不能唯一识别真实类间转移矩阵。要声称“从A转到B”，必须有同实体类别轨迹或额外可识别假设。
- `label_dictionary` 必须固定类别ID、背景值和编码区间；0–4、1–5、0背景等编码不可静默拼接。

## 7. 输出空间与解释语义

- 分类/boosting/解释结果保存 `output_space`（probability/logit/raw margin/class score等）、`class_id` 与 link。数值落在0–1之外时不得仍称概率。
- SHAP/局部解释是相对某 baseline 的模型输出分解；单实例方向不自动成为总体因果或政策效应。
- 算法标题、图名和文字描述与实际 primitive 冲突时，以可执行 primitive + 输入输出为证据，并保留语义漂移错误模式。

## 8. 事件算子、数组与跨接口合同

- 极端事件必须显式记录 upper/lower tail、阈值、联合/条件定义、观测间隔和有效暴露；用边界反例检查CDF/重现期。
- shape/length相同不等于实体或坐标对齐。空间数据还要核 CRS、transform、extent、resolution、NoData；表数据要核唯一键与排序。
- 跨CSV/程序边界必须验证header、dtype、shape和真实读取文件。源文件hash不能替代实际求解器输入的hash；若生产链集成回归未完成，保持候选/待验证状态。

## 证据边界

这些规则来自 Dev 审计、局部算术重放和合成机制反例。它们提升的是决策/审计合同，不等于 S013–S016 作者方法完整复现，也不建立 MathModel-Core 的因果能力增益。Controlled `No-Core / Previous-Core / New-Core` 仍需同 base model、prompt、tools、budget、randomness 和 evaluator 的固定 harness。
