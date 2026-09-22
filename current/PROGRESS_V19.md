# Graduate MathModel Learning Skill v1.9 训练进度

## 本轮定位

v1.9 在 v1.8 基础上继续做真实增量训练，重点不是增加论文数量，而是把 **2025 E 同题三篇优秀论文 + G老师/G老师2代码型补充资料 + 图表论证规则** 连接成可检索、可迁移的知识结构。

## 1. 保持不变的实验边界

- 45 篇论文总量不变。
- train/dev/test 仍为 **32/7/6**，同题不跨组。
- 2025 E 的 S039/S040/S041 仍属于训练组。
- G老师/G老师2仍标记为 `train_supplemental`，不计入45篇，不冒充优秀论文官方代码。
- 测试组没有被打开或用于本轮规则学习。

## 2. 2025 E 三篇优秀论文核心精读

### S039《基于迁移学习的高速列车轴承故障诊断研究》

- 93 页全文文本已读。
- 93 页低分辨率全页视觉扫描完成。
- Q1：39候选特征，Pearson/Spearman、PCA、RF重要性、互信息/卡方筛至14；突出“特征筛选证据链”。
- Q2：SVM/RF/MLP 与 VGG/CNN 竞争；五折CV。记录了重叠窗口+随机五折可能带来的文件级泄漏风险。
- Q3：CNN + 决策边界/分布对齐；MMD、CORAL与DDM。
- Q4：MMD/CORAL/DDM+t-SNE解释迁移。
- 未完成：官方原始数据端到端代码复现。

### S040《无监督迁移学习下的轴承故障诊断建模与优化》

- 69 页全文文本已读。
- 69 页低分辨率全页视觉扫描完成。
- Q1：48k→32k；TVFEMD+GWO-MOMEDA；SMOTE；36特征+MixHop。
- Q2：RF/LSTM/CNN/ViT；除单次性能外增加10次稳定性箱线图。
- Q3：KDE先证域偏移，ViT + MMD/CORAL高阶/二阶联合匹配。
- 已保留原有数值复核：正文称平均置信度0.992，但表6-2的16值等权均值为 **0.9246875**；仅判定该汇总口径矛盾，不外推为整篇模型无效。
- Q4：迁移前后embedding、域距离/质心方差、attention。
- 未完成：官方原始数据端到端代码复现。

### S041《高速列车轴承智能故障诊断问题》

- 46 页全文文本已读。
- 46 页低分辨率全页视觉扫描完成。
- Q1：32k；1024/512滑窗；SNR/RMS/crest筛样并保留10%低分；机理特征+ViT 128d。
- Q2：KNN/TCN/DenseNet/ResNet-CBAM；6:4、7:3、8:2多协议比较。
- Q3：源域统计Z-score、MIC、ResNet-CBAM+DANN+MMD+聚类/伪标签。
- Q4：事前结构/机理→迁移过程→SHAP全局/单样本解释。
- 记录边界：MMD、内聚性、跨域匹配度与目标置信度都不是无标签目标域accuracy。

对应新知识卡：

- `knowledge_base/paper_reviews/2025-E-S039-core.json`
- `knowledge_base/paper_reviews/2025-E-S040-core.json`
- `knowledge_base/paper_reviews/2025-E-S041-core.json`
- `knowledge_base/figure_argumentation/2025-E-S039.json`
- `knowledge_base/figure_argumentation/2025-E-S040.json`
- `knowledge_base/figure_argumentation/2025-E-S041.json`

## 3. 同题横向路线图

新增：

`knowledge_base/cross_paper_maps/2025-E-S039-S041-with-code.json`

按 Q1–Q4 显式比较：

- 三篇优秀论文各自路线；
- G老师/G老师2可对应的代码阶段；
- 最小基线；
- 什么时候升级复杂模型；
- 什么指标不能越界解释；
- 新题应该怎么局部复用。

核心选择规则：

- Q1：轻噪声优先简单机理/特征基线；只有故障频率被噪声遮蔽时再升级复杂去噪。
- Q2：先RF/MLP等低成本基线；深模型必须在**文件/工况级**验证上稳定胜出。
- Q3：源模型直推→CORAL/MMD→必要时DANN/伪标签，逐层做消融。
- Q4：至少区分域级对齐证据与样本/特征级解释证据。

## 4. G老师2的185页“完整论文”进一步核对

原PDF SHA256：

`491687f7691b5300f00eab1dcd9c0625b1bc9416cbb20cfa95c8cc0d6a0be266`

发现：

- PDF无可用正文文本层，因此没有用OCR强行识别185页；正文/结果页使用视觉审查。
- 核心正文/结果约在物理页1–17、21–35。
- **物理页18–20为科研服务/竞赛培训广告，与解题无关，已排除训练。**
- 约36–185页主要为代码截图/代码清单；代码学习以随包真实 `.py/.m` 为主，而不是截图OCR。
- 正文中的谱峭度/包络/故障频率、机理滤波组与gate、CORAL+entropy、两次目标预测融合，均可与随包真实代码形成强方法级对应。

新增：

`knowledge_base/code_cases/2025-E-GTeacher2-paper-code-map.json`

注意：这仍是教师/专家材料，不是S039/S040/S041的官方代码。

## 5. 相似赛题检索升级

`mathmodel-case-retriever` 现在在命中存在已审计补充代码的 `case_group` 时返回：

- `supplemental_code_cases`
- Q1–Q4 `question_links`
- code card
- run/review status
- warning

实测查询：

> 高速列车轴承 源域有标签 目标域无标签 MMD CORAL DANN 迁移学习 故障诊断

前3个结果依次命中 S040、S039、S041，并自动附带 GTeacher1/GTeacher2代码映射。

## 6. 图表学习升级

新增：

- `data-cleaning-and-visualization/references/evidence-role-figure-design.md`
- `scripts/evidence_figure_templates.py`

抽象出5类高价值图表结构：

1. 同一信号的机理四联图；
2. 特征筛选证据链；
3. 统一尺度混淆矩阵；
4. 重复运行稳定性箱线图；
5. 迁移前后embedding、目标概率热图及解释图。

每张图先定义：

`purpose / evidence_role / cannot_prove / comparison_unit`

**不固定每问画几张图，不复制优秀论文的固定配色。**

实际用合成数据做了5张模板烟测图并人工查看；最初混淆矩阵共用色条发生重叠，已修改布局后重绘通过。这些图只用于测试模板，不是比赛结果证据。

## 7. 新增可迁移错误模式

- `overlapping-window-split-leakage.json`
  - 重叠滑窗后随机划分产生近重复样本泄漏。
- `preprocessing-before-split-leakage.json`
  - 特征筛选/SMOTE/标准化在split前fit造成信息泄漏。
- `unlabeled-target-metric-overclaim.json`
  - confidence/MMD/t-SNE/cluster cohesion等内部指标被误写成目标域准确率。
- `unsupervised-bearing-domain-adaptation.json`
  - 抽象出无监督轴承域适应的分层模型阶梯和验证规则。

## 8. 回归与可运行检查

已通过：

- learning workspace validation：PASS
- 45篇论文 library validation：PASS，6752 chunks，split=32/7/6
- v1.6 已有已知缺陷回归：**18/18 PASS**
- v1.9 supplemental code retrieval regression：PASS
- v1.9 training regressions：**16/16 PASS**
- 5类图表模板：导入、生成、非空文件检查 PASS；生成图已做人工视觉抽查

没有运行的内容：

- 6篇测试论文的独立建模评估：**NOT RUN**
- 2025 E官方原始MAT上的三篇论文端到端复现：**NOT RUN**
- GTeacher2完整训练/迁移：缺原始/预处理数据，**NOT RUN**

## 9. S001状态

S001没有被虚假升级：

- 68页提取文本已读；
- Q2使用官方附件2做过真实数据局部复现；
- 39图尚未全部逐图视觉核验；
- 当前工作区没有S001原PDF，只保留部分原页和视觉审查sheet；
- Q1/Q3/Q4完整复现仍未完成。

因此它仍是“高质量局部复现样板”，尚不是完整gold-standard封版。

## 下一步

从 **S002** 继续训练组逐篇推进。新规则固定为：

**全文逐问 → 模型竞争 → 公式/代码映射 → 防泄漏验证 → 图表purpose/cannot_prove → 能运行就运行 → 风险/错误卡 → 新题局部迁移总结。**
