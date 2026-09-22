# 2024-B S006 论文—打印附录审计

## 证据边界

S006（B24103530099）共104页。本轮读完全文文本层和打印附录；没有作者原始工程/官方数据，不宣称复现。对 RandomOverSampler 的维度契约另做最小 API 烟测。

## Q1

优点是同时比较 RF 与 GBDT，并以 MSE/R²选择模型。但打印代码在 split 前用 `TargetEncoder(loc_bss_id, seq_time)` 拟合全数据，验证目标发生泄漏。正文强调 DBSCAN 与随机扰动，打印主代码没有相应 DBSCAN 路径；最终测试预测反而直接加 `np.random.normal` 高斯噪声且未固定 seed。输出噪声不能证明模型鲁棒。

## Q2

S006 将 `(NSS,MCS)` 融合为单一多分类标签，这一点比 S005 “预测 PHY Rate 再反推组合”更能避开多对一映射歧义。

但打印代码存在三重验证风险：TargetEncoder 在全体样本上 fit；StandardScaler 在 split 前 fit；RandomOverSampler 在全数据上扩增后再 split。后者会让同一少数类样本的复制体同时进入训练和验证，从而使 99.57% accuracy 不能作为可信泛化证据。

此外打印顺序先把 X reshape 为三维 CNN 张量、y one-hot，再调用 RandomOverSampler。使用 imbalanced-learn 0.14.1 的最小烟测，三维 X 直接触发 `ValueError: Found array with dim 3, while dim <= 2 is required`。安全顺序是：split -> train-only supervised encoding/scaling -> train-only resample on 2D X + 1D y -> reshape/one-hot -> CNN。

SINR 仍直接对 dBm 风格 RSSI 做差/和，并在无法判断同步异步时用无 seed 的随机选择；应回到线性功率域并把传输类型判定设计为确定性规则或有校准的概率模型。

## Q3

论文提出“双层交叉预测”：第一层 RF 预测 `num_ppdu/ppdu_dur/seq_time/other_air_time`，第二层残差网络预测 throughput。结构上比直接回归更具可解释性，但验证方式存在 oracle-intermediate mismatch。

第二层在训练/验证时使用真实中间变量，而实际测试时使用第一层 RF 预测的中间变量。于是图6-4/6-6 中接近1的 R²只说明“给真实中间变量时第二层很好”，不能说明完整级联很好。正确 stacking 应对训练集做 K-fold 第一层 OOF 预测，用这些 OOF 中间量训练第二层，然后在完全未见过的 group 上评价全链。

尤其部分第一层变量 R² 只有约0.61–0.74，必须分析它们的误差向 throughput 的传播与敏感度。

## 新题复用

- Q2 可复用“直接联合标签”思想，但验证采用 group split + train-fold-only balancing。
- Q3 可复用“中间物理变量 -> 最终吞吐量”的分层结构，但要用 OOF stacking，并同时保留 direct baseline。
- 所有声称鲁棒性的随机扰动必须发生在可解释的训练/概率建模流程中，不能在最终提交值上随意加噪声。
