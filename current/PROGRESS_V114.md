# PROGRESS V1.14

## 本轮范围

在 v1.13 基础上完成 2024-B 训练论文 S006（B24103530099，104 页）的全文文本层、打印附录静态审计和最小 API 兼容性烟测，并将其与 S005 建立同题横向方法图谱。

## S006 已完成

- 104/104 页全文文本已核心审查。
- Q1–Q3 建立方法路线、优点、风险、迁移规则。
- 30 条显式图题建立论证角色索引；没有原 PDF 像素，因此未宣称完成配色/版式像素级学习。
- 打印附录完成静态审计；作者原始工程和官方数据未取得，不宣称完整代码复现。
- 对 `RandomOverSampler` 的 3D 输入做最小 API 烟测：imbalanced-learn 0.14.1 明确拒绝三维 X。

## 新增关键门禁

1. TargetEncoder 等监督编码：split-first + train-only + OOF/cross-fit。
2. RandomOverSampler/SMOTE/ADASYN 只在训练折内执行，验证/测试保持自然分布。
3. 重采样器先做 X/y 形状契约烟测；表格重采样后再 reshape/one-hot。
4. 两阶段/stacking/cascade 第二层必须使用第一层 OOF 预测作为训练中间量。
5. 必须报告完整级联端到端指标与误差传播，不用“第二层 oracle 中间量高分”代替。
6. 最终预测上直接加随机噪声不等于鲁棒训练；无固定 seed 的提交输出不可复现。

## S005 vs S006 方法竞争

### Q2
- S005：先预测 PHY Rate 再反推 (MCS,NSS)，存在非单射映射问题。
- S006：直接把 `(MCS,NSS)` 融合成联合类别，结构上更合理。
- 但 S006 的过采样、TargetEncoder、Scaler 顺序导致验证泄漏，因此“方法结构更合理”不能等同于“论文给出的 99.57% 泛化准确率可信”。

### Q3
- S005：直接 CNN 回归 throughput，结构简单。
- S006：RF 预测中间帧统计量，再用残差网络预测 throughput，可解释性更强。
- 正确比较必须加入 OOF stacking 和 end-to-end holdout；否则 S006 的第二层 R² 不能代表完整级联。

## 图表能力新增

新增并实际烟测：
- `cascade_oof_validation`：并排展示 direct baseline、oracle stage-2 和真正端到端 OOF cascade。
- `resampling_partition_diagnostic`：展示训练集重采样前/后与 untouched validation 的类别分布。

## 回归

- v1.14 S006 专项：24 项 PASS。
- v1.14 2024-B 检索：PASS。
- v1.10/v1.11/v1.12/v1.13/v1.14、v1.6、v1.8、v1.9 历史核心回归：PASS。
- v1.9 code-link：PASS。
- 全库：45 papers / 6752 chunks / 32 train / 7 dev / 6 test，冻结 split hash PASS。

## 回归脚本修正

v1.13 旧测试原先写死 `papers_reviewed == ['S005']` 和 `VERSION == 1.13.0`，这会在合法加入 S006、升级版本时误报退化。已改为真正的历史不变量：S005 仍保留在 reviewed 且版本至少为 1.13。

## 下一步

进入 S007（2024-B 第三篇）全文与打印附录审查，扩展同题方法族到 S005/S006/S007。
