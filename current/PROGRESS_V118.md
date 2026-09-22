# PROGRESS V1.18

## 本轮范围

在 v1.17 基础上完成 2024-C 训练论文 S010（C24103860012，82 页）的全文文本核心精读、打印附录静态审计与 Q5 类别编码辅助函数精确烟测；继续扩展 2024-C 的 S009–S012 同题方法族。

## S010 已完成

- 82/82 页全文文本核心精读。
- Q1–Q5 建立模型路线、优势、风险、代码证据和迁移规则。
- 32 条显式图题、33 条表题建立论证角色索引；当前没有源 PDF 像素，不宣称真实配色、字体、线宽和版式已逐像素学习。
- 打印附录完成静态审计；作者原始工程和官方数据未取得，不宣称端到端复现。
- Q5 可见类别编码辅助逻辑已精确烟测：12 个波形×材料合法组合在打印逻辑中均塌缩成全零类别向量。

## 关键学习

1. **交叉验证必须对齐真实泛化单位**：随机行 KFold 只能说明同分布插值；跨温度/材料/设备等结论要用 grouped 或 leave-condition-out。
2. **非显著不等于独立**：Q3 两个交互项 p>0.05 不能据此积极断言因素相互独立；应报告交互估计、区间与统计功效。
3. **特征变换也属于 schema contract**：正文说 log(Bm)，打印 Q4 却把 raw maxB 输入 CatBoost；raw/log/normalized、dtype 和类别 vocabulary 都需统一。
4. **论文最佳模型必须有完整可执行路径**：正文最佳是 CatBoost+IGSE，但打印代码只展示较简单的五基本特征 CatBoost；kurtosis/skewness 虽计算却未进入 X，也没有 IGSE 拼接路径。
5. **均值指标必须核对 denominator**：打印 `true_mse` 实际累计平方误差但未除样本数，不能命名为 Mean Squared Error。
6. **1:1 数字权重不等于等偏好**：Q5 直接使用 `predicted_loss - f*Bm` 混合不同单位/尺度，必须先无量纲化或保留 Pareto/epsilon-constraint。
7. **类别编码需要 deployment 单元测试**：可见 objective 先把整数类别映射成中文字符串，再交给只匹配整数的 one-hot helper，导致类别位全部为0。
8. **优化器排名必须有同预算、多 seed、完整实现证据**：正文比较 GA/PSO/GWO，但打印附录只有 PSO；且 visible PSO 固定 T=25、波形=3、材料=1，不能直接支撑 T=70/90 和48组合结论。
9. **指标名称/方向要注册**：EMI = loss/(loss+energy) 数值越小越好，本质更接近损失占比，不能未经解释称为“效率最大化指标”。
10. **不要用未调整因素分析提前剪掉离散变量**：Q3 的低损耗组合受频率/Bm 分布影响，不应在完整 Pareto 搜索前永久固定材料/波形。

## 新增知识资产

- `knowledge_base/paper_reviews/2024-C-S010-core.json`
- `knowledge_base/code_cases/2024-C-S010-appendix-code.json`
- `knowledge_base/figure_argumentation/S010.json`
- 更新 `knowledge_base/cross_paper_maps/2024-C-S009-S012.json`
- `knowledge_base/error_patterns/categorical-encoding-type-mismatch.json`
- `knowledge_base/error_patterns/unnormalized-weighted-objective-scale-dominance.json`
- `knowledge_base/error_patterns/computed-feature-not-used.json`
- `knowledge_base/error_patterns/metric-name-direction-mismatch.json`
- `knowledge_base/error_patterns/mean-sum-metric-mislabel.json`
- `.agents/skills/graduate-mathmodel-learning/references/2024-C-S010-paper-code-audit.md`
- `learning_output/analyses/v118_S010/q5_feature_contract_smoke.json`

新增图表论证模板：

- 泛化单位/CV 划分审计图；
- 类别编码 contract 图；
- 多目标尺度/标量化敏感性图。

图表模板学习证据结构，不复制某篇论文固定配色。

## 回归

- v1.18 S010 专项：39 项 PASS。
- v1.18 2024-C S010 实际检索烟测：PASS。
- v1.6–v1.18 graduate 核心历史回归：PASS。
- v1.9 code-link、2024-A、2024-B、2024-C 历史检索回归：逐项 PASS。
- 全库验证：PASS，45 papers / 6752 chunks / 32 train / 7 dev / 6 test；group isolation、frozen split hash、chunk/page roundtrip、review bounds、train-only retrieval smoke 全部 PASS。

## 诚实边界

本轮仍不代表 45 篇全部精读完成。S010 未取得作者原始工程、官方附件和源 PDF 像素，因此是“全文文本 + 打印附录静态审计 + Q5 类别辅助函数精确烟测”，不是完整数值复现或像素级论文风格复现。

## 下一步

进入 2024-C 训练论文 S011，继续比较：Q1 波形识别是否采用不同特征/模型、Q2 温度修正是否真正做跨温度验证、Q3 是否控制频率/Bm、Q4 物理+数据驱动模型的最终执行路径，以及 Q5 是否真正实现混合变量 Pareto/多目标优化并满足可行域。
