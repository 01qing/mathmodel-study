# v1.17 学习进度：2024-C S009 全文/打印附录审计与优化可行性门禁

## 本轮定位

v1.17 继续沿用冻结的 45 篇优秀论文语料与 32/7/6 训练/开发/测试划分。本轮只学习训练组中的 2024-C S009，不打开测试组论文，不改变冻结分组。

“学习/训练”指更新 Skill、知识卡、错误模式、检索映射、图表论证模板和回归门禁，不修改基础模型参数。

## S009 已完成内容

- 论文：`S009`，2024-C，71 页，训练组。
- 已完成 71/71 页全文文字层核心精读。
- 已按 Q1-Q5 建立方法、优势、风险和迁移建议。
- 已审计打印附录代码；缺原始工程/数据的 Q1-Q4 不标记为作者流水线复现。
- Q5 可自包含打印片段已进行真实烟测。
- 已建立 22 个显式图题与 32 个表题的论证角色索引；由于当前没有源 PDF 像素，不宣称完成配色、字体、线宽等像素级风格学习。

## 关键学习结论

### Q1 波形分类

论文主线为手工波形特征 + MLP / Random Forest + 声称的加权融合。打印代码与正文存在明显特征契约漂移：训练前特征、分类器输入 `X`、推理阶段 mean/peak/std 三者不能形成可复现的统一 schema；RF 树数也与正文不一致，且未看到融合实现。

新增门禁：训练、验证、测试、推理必须绑定同一特征 schema，列名、顺序、单位、变换和版本均可追溯。

### Q2 温度修正 Steinmetz

保留 Steinmetz 物理基线是优点，但多个温度修正模型主要用同一数据拟合后再比较 MAPE/R²。参数与公式在正文、表格、打印代码之间还有符号/科学计数法漂移。

新增门禁：物理参数建立唯一参数注册表；模型选择优先采用留一温度/留一工况验证，而不是拟合内指标。

### Q3 因素与交互作用

论文用 ANOVA 回答温度、波形、材料及交互，但直接对原始磁芯损耗建模，没有控制频率和磁通密度 Bm 两个强连续协变量。因此显著性可能混入工况分布差异；p 值也不能充当效应大小。

新增门禁：因素分析先做协变量调整（如 log f、log Bm），再报告调整后边际效应/效应量/置信区间。

### Q4 12 个材料×波形模型

分区物理模型有可解释性，但需要统一参数表、路由条件、支持域和跨工况验证。论文表格存在同一参数跨表不一致，打印附录只展示单个文件/单个分区拟合，不足以证明完整 12 路部署。

### Q5 双目标优化

论文声称混合整数 PSO，并把温度、频率、Bm、波形、材料作为变量；打印代码实际为 `scipy.optimize.minimize`，只有 f/Bm/U 三个连续变量。

打印代码边界：

- f ∈ [50000, 320000]
- Bm ∈ [0.1, 0.3]
- U ∈ [25, 90]

对可自包含打印片段进行真实运行后，求解器成功返回近似：

- f = 50000
- Bm = 0.1
- U = 90
- P/Q ≈ 321991.3178

论文报告的频率 694891/813076 超过打印代码 f 上界，线性结果温度 22 低于 U 下界，因此这些论文点不能由该打印可行域直接产生。打印代码中 `f**2.7181` 也与附近的 α≈1.7181 存在参数冲突。

这只是“可见打印片段的精确烟测”，不能冒充作者完整 PSO 工程复现。

新增门禁：优化结果必须做可行域 replay、约束 slack、参数注册、支持域距离和目标函数回代；双目标优先输出 Pareto/ε-constraint 证据，再按声明的偏好选点。

## 新增知识资产

- `knowledge_base/paper_reviews/2024-C-S009-core.json`
- `knowledge_base/code_cases/2024-C-S009-appendix-code.json`
- `knowledge_base/figure_argumentation/S009.json`
- `knowledge_base/cross_paper_maps/2024-C-S009-S012.json`
- `knowledge_base/error_patterns/feature-contract-train-inference-drift.json`
- `knowledge_base/error_patterns/factor-analysis-covariate-confounding.json`
- `knowledge_base/error_patterns/parameter-registry-transcription-drift.json`
- `knowledge_base/error_patterns/optimization-result-outside-feasible-domain.json`
- `.agents/skills/graduate-mathmodel-learning/references/2024-C-S009-paper-code-audit.md`
- `learning_output/analyses/v117_S009/q5_printed_code_smoke.json`

新增图表论证模板：

- covariate-adjusted interaction plot
- optimization feasibility replay

图表模板学习的是证据结构，不复制某篇论文固定配色。

## 与既有 2024-C 独立路线的关系

项目中已存在 2024-C 的历史独立方案/代码审计材料，但该材料不是全新盲测，原因是此前已经有公开代码暴露。v1.17 保留这个污染标签，不把它重新包装成严格 blind baseline。

S009 与独立路线的主要组合建议：

- Q1：保留可解释的波形特征，但固定 schema 并采用分组/跨工况验证。
- Q2：保留 Steinmetz 基线，但用留一温度选择修正形式。
- Q3：从原始损耗 ANOVA 升级为含 log f、log Bm 的 ANCOVA/稳健模型。
- Q4：物理模型作为 baseline，与全局/混合数据驱动模型做跨工况验证。
- Q5：从单一 P/Q 比值点升级为显式双目标 Pareto/ε-constraint，并做可行性和支持域审计。

## 验证结果

- v1.17 S009 专项回归：PASS。
- 2024-C S009 实际检索烟测：PASS。
- 全库验证：PASS，45 篇、6752 个片段、32 train / 7 dev / 6 test。
- 冻结 split hash 与同题隔离：PASS。
- 历史 v1.6-v1.16 核心回归：PASS。
- 2024-A、2024-B 历史检索回归：PASS。
- 2024-C 新检索回归：PASS。

## 仍未完成

- S009 源 PDF 的逐像素视觉风格审查未完成，因为当前工作区没有可用源 PDF 像素。
- S009 原始工程和官方数据未完成作者端到端复现；除 Q5 可自包含打印片段外，其余只做静态代码审计。
- S010-S012 尚未逐篇精读；v1.18 起继续 2024-C 同题方法族学习。
