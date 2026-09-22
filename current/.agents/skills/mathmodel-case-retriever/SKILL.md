---
name: mathmodel-case-retriever
description: 新数学建模题出现时，按子问题检索历年赛题论文中可迁移的局部结构，返回原文页码、相似点、关键差异和待验证条件。适合询问“像哪年哪题哪篇论文”或跨论文寻找方法依据；不代替graduate-mathmodel-learning选模或原正式比赛流程。
---

# 相似赛题与局部方法检索

这是graduate-mathmodel-learning的配套检索Skill，沿用户v1.5→v1.6→v1.7主线添加，不接管正式建模流程。

## 工作顺序

1. 先读新题，逐问写出输入数据、输出目标、约束、标签状态和拟验证的推广范围。已有problem_analysis.json时复用。检索前保存这些题目事实，避免看过答案后反向解释新题。
2. 对每一问分别检索。查询用完整的结构描述，必要时分成“任务与数据”和“约束与验证”两个查询，不只输入算法名或题材名。
3. 运行 `scripts/search_cases.py --query "..." --mode production --top 6`。根据输出的paper_id/page，用 `scripts/read_paper.py --paper-id Sxxx --pages 12,13` 阅读完整相关页，必要时查看原PDF图表和公式。搜索片段只是候选证据。
4. 若该paper_id已有knowledge_base/case_analogies和paper_reviews记录，先读其已核验反例与适用限制；未完成评审的候选须明确标注。按任务结构、数据形态、目标/约束、假设和验证边界做判断。区分同题材不同数学问题与不同题材同数学结构。论文中出现某算法不代表它适用于新题。
5. 给每问保留少量有证据的候选，并明确“可迁移部分”和“必须重做部分”。同一题的多篇论文应比较差异，不能当多份独立证据累加信心。没有足够相似依据时说明仅存在一般方法联系或没有可靠匹配。
6. 把匹配结果交回graduate-mathmodel-learning进行基线/替代模型竞争和反例检验。正式模型路线与PASS仍由原项目管理。

## 给用户的输出

用普通中文说清：
- 新题第几问，与哪年哪题的哪篇论文、哪一节/页相似。
- 相似的是数据结构、目标、约束或某个子步骤，而非笼统“很像”。
- 能借鉴的建模思路、需要修改的条件、不能照搬的地方。
- 若案例有已审计代码：指出可借鉴的具体代码阶段/函数、输入输出接口、已知缺陷与运行状态。
- 若案例有已审计图表：指出可复用的是哪种证据结构（如误差对比、消融、置信度一致性、敏感性），不是只模仿配色。
- 最小验证实验，以及什么结果会让我们放弃这条迁移路线。

不输出“相似度87%所以适用”一类结论。脚本的lexical_cosine是检索排序量，不是适用概率、科学置信度或获奖概率。参数默认值属于检索工程设置，不是已证最优设置。

## 训练/开发/测试边界

读 [evaluation-protocol.md](references/evaluation-protocol.md)。45篇按整道赛题分为32/7/6，划分记录及SHA256在assets/split_manifest.*。此前已接触部分内容，均不称干净盲测。

普通 `--mode evaluation` 与 `--mode production` 均只允许从 **reviewed Train pages** 拟合和检索。Dev 不进入普通检索，只能走“freeze Core → problem/data independent solution freeze → Dev paper comparison → generic-rule update”的专门开发验证流程；Test 在独立答案冻结前不得进入答案检索。索引中的未 reviewed Train pages 也不能进入普通 Core 检索。

## 逐篇学习的真相源

assets/papers.json记录全文索引状态；它不证明已经读过全文。逐篇评审写入graduate-mathmodel-learning已有paper_review格式，扩展结构信息另写knowledge_base/case_analogies/，不要修改旧schema来容纳随意字段。
未完成的论文保留not_reviewed/core_partial等明确状态；只有逐问覆盖正文并登记页码、公式、结果、验证和局限后才称core_reviewed。附录检查与代码复现另计。不得把自动提取、关键词标签或批量生成卡片称为45篇已经精读。

运行脚本需要Python、NumPy、scikit-learn；阅读PDF图像时按可用PDF工具处理。大篇论文分段读取，用返回的截断提示继续；全文按页保存在assets/pages，原PDF位置和哈希在assets/papers.json。

## 全文精读和独立作答要求

开展逐篇学习或测试时，读取[full-paper-study-protocol.md](references/full-paper-study-protocol.md)。用户范围已升级为全文及附录，图表数量/构图/论证和可运行复现分别登记；测试必须先独立完成并冻结答案，再看论文。

## 代码型补充案例

当 `knowledge_base/code_cases/` 存在与候选题相关的记录时，必须与论文页码证据一起读。代码型教师/作者资料属于补充训练证据，不新增到45篇论文计数，也不能改变原 split。命中时返回：代码链、运行级别、图表模板、已知 bug、数据依赖和不能外推的结论。完整规则见 `graduate-mathmodel-learning/references/code-paper-figure-learning.md`。


## 补充代码映射（v1.9）

检索结果若命中有已审计补充代码的 `case_group`，`search_cases.py` 会返回 `supplemental_code_cases`。

必须遵守：
- 只把它作为**方法级实现线索**；不得说成命中论文的官方代码。
- 新题按子问题引用 `question_links`，并同时显示 `warning`。
- 优先给“可复用代码阶段 + 已知风险 + 最小验证实验”，不要只给仓库路径。
- 2025 E 命中时，结合 `graduate-mathmodel-learning/references/2025-E-cross-paper-code-figure-map.md` 做三篇论文横向比较。

## v1.15：2024-B 第三篇已审计提示

命中 `2024-B` 时同时读取 `knowledge_base/cross_paper_maps/2024-B-S005-S008.json`。S007 可提供正确的 dBm→mW SINR 实现线索，但其 MCS/NSS 独立预测缺少联合合法性约束，且 NSS 存在“Accuracy≈0.98、F1/Precision/Recall≈0.55”的类别不平衡信号。检索输出必须同时提示这些可借鉴点与风险，不能只引用高准确率。

## v1.19：2024-C 第三篇审计提示

命中 `2024-C` 时同时读取 `knowledge_base/cross_paper_maps/2024-C-S009-S012.json`。S011 的可借鉴点是“温度修正族比较 + 明确保留 Pareto 前沿”，但检索输出必须同时提示：Q3 交叉均值不等于协同交互；Q4 打印“Bi-LSTM”代码实际上为 CNN-only 且 1033/10 维特征契约冲突；Q5 权重 `a` 被当成决策变量、打印附录没有 Q5 优化代码、报告 MOPSO 样例存在越界，且“Pareto 点更集中”不能证明算法更优。新题应借 Pareto 思路而不继承这些证据缺口。

## v1.31：2025-C S032-S033 provisional retrieval guidance

命中 `2025-C` 时读取 `knowledge_base/cross_paper_maps/2025-C-S032-S036.json`，当前仅 S032/S033 已审计，S034-S036 仍 pending。现阶段可迁移主线是：Q1 将预测精度赢家与部署推荐分开；Q2 优先未知实例数的拓扑分组 + 固定物理周期 + 有界鲁棒拟合/reject；Q3 先验证 ordered physical profile 与 canonical JRC，再谈自适应/Z3；Q4 将兼容分数、概率、Bernoulli 熵和 expected information gain 分开，并先 replay 所有硬约束。不得把 S033 的同对象自拟合“神经网络”、固定3类GMM、模拟裂隙输入或局部熵热点当成已验证通用模块。
