# PROGRESS V1.16

## 本轮范围

在 v1.15 基础上完成 2024-B 训练论文 S008（B24116640167，69 页）的全文文本核心审查与打印附录静态审计，并将 2024-B 的 S005/S006/S007/S008 四篇训练论文闭环为同题方法族。

## S008 已完成

- 69/69 页全文文本核心审查。
- Q1–Q3 建立模型路线、优势、风险、代码证据和迁移规则。
- 64 条显式图题建立论证角色索引；当前没有原 PDF 像素，因此不宣称真实配色、字号、线宽和版式已经逐图学习。
- 打印附录完成静态审计；作者原始工程和官方数据未取得，不宣称作者 pipeline 已实际复现。
- 新增 `2024-B-S008-paper-code-audit.md`，把论文叙述、打印代码、结果表和跨论文推荐统一到一个可复核入口。

## S008 关键学习

1. **RNN/LSTM 必须具有真实序列轴**。S008 把独立表格样本 reshape 为 `(n,1,p)`，时间步 `T=1`，虽然能够调用 LSTM 层，但没有历史序列供循环状态学习，不能将结果解释为“长期依赖/时序记忆”。
2. **多干扰 SINR 必须在线性功率域求和**。打印代码直接执行 `rssi_0-rssi_1-rssi_2`，对 dBm 对数功率不成立。
3. **PHY Rate→(MCS,NSS) 不是单射**。表中多个 PHY Rate 对应多个合法组合，按排序/字典顺序 floor lookup 不能提供唯一物理证据。
4. **级联模型必须训练部署一致**。Q3 训练证据依赖真实中间变量，而部署时依赖 Q1/Q2 预测中间变量；应使用 OOF 上游预测训练下游，并在 untouched experiment groups 上整链评估。
5. **核心指标先做代数 sanity check**。表中 3AP polynomial-SVR 报告 `MSE=12.48, MAE=7.30`，但同一误差向量必有 `MSE>=MAE^2`，而 `7.30^2=53.29>12.48`，所以至少一项数值/标签有误，不能用于选模。
6. **物理公式先作为明确 baseline**。S008 的 `throughput≈PHY Rate*(1-PER)*seq_time/test_dur` 应优先保留，再检验 ML 是否在独立实验组上带来稳定残差改进。

## 2024-B 四篇最终组合建议

### Q1 seq_time

优先使用 group-aware RF/GBDT/XGBoost 作为稳健基线。只有数据存在明确实体/会话顺序、窗口 `T>1`，并且时序模型对匹配特征的 MLP/树模型有独立留出增益时，才升级到 RNN/LSTM。

### Q2 MCS/NSS

组合路线为：

- S007 的 dBm→mW/W 线性功率 SINR；
- S006 的联合 `(MCS,NSS)` 合法类别表示；
- train-only 类别平衡处理；
- group-aware 验证；
- macro/per-class F1、balanced accuracy、joint exact-match 和 invalid-pair rate。

避免 S005/S008 的“先预测 PHY Rate 再非单射反演 MCS/NSS”。

### Q3 throughput

先建立 S008 的机理吞吐量 baseline，再比较 residual ML / direct ML。若 Q3 依赖 Q1/Q2 输出，训练阶段必须使用 OOF 上游预测，最终在 untouched groups 上从 Q1→Q2→Q3 整链验证。

## 新增门禁

- single-timestep RNN/LSTM pseudo-sequence gate；
- metric algebra sanity gate；
- physics-baseline-before-black-box gate；
- multi-interferer linear-power SINR gate；
- non-injective target reconstruction gate；
- deployment-consistent OOF cascade gate。

## 回归

- v1.16 S008 专项：27 项 PASS。
- v1.13/S005、v1.14/S006、v1.15/S007、v1.16/S008 的 2024-B 检索回归：全部 PASS。
- 2024-A 历史检索回归：PASS。
- v1.6–v1.16 graduate 核心历史回归：PASS。期间修复 v1.15 旧测试把“当时仅精读 S005–S007、S008 pending”写成永久不变量的问题，改为检查历史已学论文持续存在且同题组成员关系不被破坏。
- 全库验证：45 papers / 6752 chunks / 32 train / 7 dev / 6 test；group isolation、frozen split hash、chunk/page roundtrip、review bounds、train-only retrieval smoke 全部 PASS。

## 诚实边界

本轮仍不代表 45 篇全部精读完成。S008 未取得作者原始工程/官方数据/源 PDF 像素，因此是“全文文本 + 打印附录静态审计”，不是完整代码复现或像素级论文风格复现。

## 下一步

进入 2024-C 训练组 S009，开始新的 case group。重点检验此前学出的数据边界、指标一致性、物理基线、模型实现证据和图表论证规则能否迁移到新的问题类型，并逐步形成 S009–S012 的同题方法族。
