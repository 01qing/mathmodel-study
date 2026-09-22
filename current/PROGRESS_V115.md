# PROGRESS V1.15

## 本轮范围

在 v1.14 基础上完成 2024-B 训练论文 S007（B24104760033，113 页）的全文文本核心审查与打印附录静态审计，并将 2024-B 方法族扩展为 S005/S006/S007，S008 仍待精读。

## S007 已完成

- 113/113 页全文文本核心审查。
- Q1–Q3 建立方法路线、优点、风险和迁移规则。
- 68 条显式图题按论证作用分类；当前没有原 PDF 像素，因此不宣称真实配色/版式已逐图学习。
- 打印附录完成静态审计；作者原始工程和官方数据未取得，不宣称完整代码复现。

## 本篇值得保留的优点

S007 的 Q2 `calculate_sinr` 将 desired/interference/noise 的 dBm 先转换成 mW，在线性功率域求和、作比，再转 dB。相较前两篇中出现的直接 dBm 运算，这是更可靠的物理实现，应作为新 WLAN 方案的计算基线。

## 新增关键门禁

1. MCS/NSS 等结构化输出用独立分类头时，必须检查合法 tuple、joint exact-match 和 invalid-pair rate；不能只看各头 Accuracy。
2. Accuracy 接近 1 而 macro/per-class F1、Precision、Recall 明显较低时，按类别不平衡警报处理，必须报告 support、混淆矩阵、balanced/macro 指标和少数类召回。
3. RSSI/dBm 的功率聚合必须回到线性功率域；dBm 上直接求和不代表功率和，算术均值也要明确统计语义。
4. 摘要、结果表、正文结论、附录/代码输出建立同一结果 registry 并自动交叉检查。
5. `1-P90(relative error)` 等题目自定义分数不得无说明地称为标准 regression accuracy。
6. 摘要/正文的模型数量和方法名必须由统一方法清单生成，避免“8种/9种”漂移。

## S007 发现的典型一致性问题

- 摘要称 Q1 使用 8 种回归模型，结果节实际比较 9 种。
- Q2 的 NSS Accuracy 约 0.984–0.988，但 F1/Precision/Recall 约 0.33–0.55；高 Accuracy 不能解释成“数据更平衡”。
- Q2 打印附录只有独立 RF 的 MCS/NSS 最终路径，没有形成正文 8 分类器全套运行证据。
- Q2 AMC 文字方向与其阈值 argmax 公式存在方向冲突，需用单调性/边界测试决定正确版本。
- Q3 正文公式/代码对多个 RSSI 的 dBm 值直接求和或算术平均，若表示功率聚合则量纲不正确。
- Q3 摘要 2AP 指标复用了 Q1 的 `10.412/1.756/0.064`；Q3 自己结果表给出 RF `1.926/0.894/0.051`、XGBoost `2.144/0.923/0.052`，随后的解释段又写回 Q1 数字，属于跨章节结果漂移。

## 图表能力新增

新增并实际烟测：

- `imbalanced_classification_dashboard`：混淆矩阵 + per-class Precision/Recall/F1/support + Accuracy/Balanced Accuracy/Macro F1，专门揭示多数类掩盖。
- `structured_pair_validity`：预测 tuple 频数矩阵 + marginal accuracy + joint exact-match + invalid tuple rate，用于 MCS/NSS 等结构化标签。

## 2024-B 三篇方法竞争

- S005 Q2：PHY Rate 后反推 MCS/NSS，有非单射问题；功率量纲也有缺陷。
- S006 Q2：联合 `(MCS,NSS)` 类别结构更合理，但 TargetEncoder/Scaler/过采样顺序泄漏，SINR 计算不可靠。
- S007 Q2：SINR 线性功率实现更可靠，但独立 MCS/NSS 分类缺联合合法性约束且类别不平衡明显。

推荐新路线不是照搬任一篇，而是：**S007 的物理 SINR + S006 的联合标签思想 + group-aware/train-only 验证 + imbalance-aware metrics**。

## 回归

- v1.15 S007 专项：26 项 PASS。
- v1.13 S005、v1.14 S006、v1.15 S007 的 2024-B 检索回归：PASS。
- v1.6–v1.15 graduate 核心历史回归：本轮逐项运行均通过；v1.14 旧测试中写死未来 `papers_reviewed` 数量的断言已改为检查 S005/S006 持续存在，避免合法新增 S007 被误判退化。
- 全库验证：45 papers / 6752 chunks / 32 train / 7 dev / 6 test；group isolation、split hash、chunk/page roundtrip、train-only retrieval smoke 全部 PASS。

## 下一步

进入 S008（2024-B 第四篇），完成 2024-B 四篇训练论文的同题横向闭环；随后再转入下一 case group。
