# v1.19 进度：2024-C S011 全文、打印附录与 Pareto/架构一致性审计

## 本轮范围

- 基线：v1.18。
- 新增训练论文：S011 / 2024-C / C24104220149，共 71 页，保持 `train` split。
- 完成：71/71 页全文核心精读、打印附录 Programs 1–4 静态审计、Q4/Q5 精确契约烟测、图表论证索引、同题 S009–S011 横向更新。
- 未声称：当前工作树没有 S011 原 PDF 像素、官方原始附件和作者完整工程，因此不宣称像素级版式学习或作者代码端到端复现。

## S011 主要方法

- Q1：时/频域特征 + PCA/非参数筛选 + SVM/决策树/Stacking。
- Q2：Steinmetz + 五种温度修正 + 最小二乘/模拟退火/PSO/动态PSO。
- Q3：单因素和交叉分组均值/方差，选择 90℃ + 正弦 + 材料4。
- Q4：正文声称“特征权重提取的 Bi-LSTM”，并与 CNN/XGBoost 比较。
- Q5：加权单目标 GA/PSO + Pareto 路线 NSGA-II/MOPSO。

## 本轮关键发现

1. **Q2 结果归因不一致**：摘要称动态 PSO 相比常值 PSO 的 R² 增加 0.041，但无修正表中二者 R² 均为 0.9448。0.9955−0.9448=0.0507 是温度修正后的模型改善，不能归因于动态 PSO 本身；并且动态 PSO 在不同修正式/指标上并非统一最优。
2. **Q3 描述性交叉表不等于交互/协同**：交叉均值、方差、箱线图只能描述单元格分布；要声称协同必须显式估计 interaction term，并调整频率、Bm 等强连续协变量。
3. **Q4 架构名与代码不一致**：打印程序2标题是 Bi-LSTM，但代码是 `CNNModel` + `Conv1d` + `Linear`，未见 `nn.LSTM`。
4. **Q4 feature contract 不一致**：正文称最终 10 维特征；程序2写死 `input_size=1033`。程序4可见 1024 个磁通密度点 + 温度1 + 频率1 + 材料4 + 波形3 = 1033；程序3传统CNN反而使用 `input_size=10`。因此模型对比同时改变了输入 schema，不能把差异纯归因于架构。
5. **K-S 语义错误风险**：正文把 statistic=0.2988 与 0.05 直接比较并据此判定“符合长尾分布”，混淆 test statistic 与 p-value/临界值语义。
6. **扰动鲁棒性 ≠ 跨工况泛化**：IID 测试集加小高斯噪声只能作为 perturbation robustness，不能替代跨材料/温度/工况 holdout。
7. **偏好权重不能由优化器自由选择**：Q5 把权重 `a` 加入决策变量，等于允许优化器改变决策偏好；应固定/扫描权重或先保留 Pareto 前沿再外部选点。
8. **显示公式无法复算表8.2**：按式(8.3)可见 raw 形式复算，GA=69.425101、PSO=11.249049，与表中的 4.6918 / 30.8623 不一致；正文虽称“归一化”，但没有可复现的归一化 contract。
9. **Pareto 示例越界**：表8.3 的一个 MOPSO 点 `Bm=0.4261>0.3133`，另一个 `f=49910<50000`。所有 Pareto/最优点必须逐点 replay constraints。
10. **Pareto 图更集中不等于算法更优**：应在相同预算、多随机种子下比较 hypervolume、IGD/GD、spread、可行率和运行代价。
11. **Q5 打印实现缺口**：附录只见 Programs 1–4，没有可见 GA/NSGA-II/MOPSO 的 Q5 实现，因此算法排名只保持 paper-claimed / implementation-not-visible 状态。

## 新增 Skill 门禁

- 描述性交叉表不得直接写成协同/交互。
- 标签驱动特征筛选必须 nested CV。
- 深度模型名称由 executable layer graph 核验。
- feature dimension / transform / input shape 纳入 feature contract。
- 检验 statistic / p-value / alpha 分开登记。
- perturbation robustness 与 domain generalization 分开命名。
- preference weight 外生化，不允许优化器自由选择自己的权重。
- “已归一化”必须能从公式/代码复算。
- Pareto 点逐点 feasibility replay。
- 多目标算法采用 HV/IGD/GD/spread/feasible-rate + 多 seed 公平比较。

## 图表学习

已实际生成两个新证据模板：

- `learning_output/analyses/v119_figure_template_smoke/01_interaction_evidence.png`：区分主效应和真实交互效应，不允许仅凭交叉均值图宣称协同。
- `learning_output/analyses/v119_figure_template_smoke/02_pareto_feasibility.png`：在 Pareto 图上显式标注可行/越界点，并要求后续配合 HV/IGD/spread 数值。

S011 文本层识别到 43 个实际图题行、28 个实际表题行；图号有 42 个唯一编号，因为文字层中 `图7.2` 出现重复编号。当前没有原 PDF 像素，因此不宣称学到了配色/字体/线宽。

## 回归状态

- `test_v119_regressions.py`：43 项通过。
- `test_v119_2024C_retrieval.py`：通过。
- `validate_library.py`：通过，45篇 / 6752 chunks / 32 train + 7 dev + 6 test，冻结 split 未污染。
- v1.17、v1.18、v1.19 的 2024-C 检索回归逐项通过。
- 历史 v1.18 测试中的“reviewed 必须恰好等于 S009/S010”被修成真正的不变量：S009/S010 必须保留，后续合法增加 reviewed 不应失败。
- 早期 v1.8 测试依赖 `cwd`；教师代码卡没有丢失，正确从 Skill 根目录运行即可通过。

## 下一步

进入 S012（2024-C 第四篇），完成全文/附录/图表/代码审计，并把 S009–S012 闭环成完整同题方法族。测试集继续冻结，不提前打开测试论文。
