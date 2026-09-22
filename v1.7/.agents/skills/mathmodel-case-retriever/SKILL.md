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
- 最小验证实验，以及什么结果会让我们放弃这条迁移路线。

不输出“相似度87%所以适用”一类结论。脚本的lexical_cosine是检索排序量，不是适用概率、科学置信度或获奖概率。参数默认值属于检索工程设置，不是已证最优设置。

## 训练/开发/测试边界

读 [evaluation-protocol.md](references/evaluation-protocol.md)。45篇按整道赛题分为32/7/6，划分记录及SHA256在assets/split_manifest.*。此前已接触部分内容，均不称干净盲测。

`--mode evaluation`只从训练组论文拟合TF-IDF和检索。开发组用于完善问题描述及错误分类；测试组只用于冻结版本后的回溯评估。production可以搜索全部45篇，但不能把生产库中的检索演示当留出测试成绩。

## 逐篇学习的真相源

assets/papers.json记录全文索引状态；它不证明已经读过全文。逐篇评审写入graduate-mathmodel-learning已有paper_review格式，扩展结构信息另写knowledge_base/case_analogies/，不要修改旧schema来容纳随意字段。
未完成的论文保留not_reviewed/core_partial等明确状态；只有逐问覆盖正文并登记页码、公式、结果、验证和局限后才称core_reviewed。附录检查与代码复现另计。不得把自动提取、关键词标签或批量生成卡片称为45篇已经精读。

运行脚本需要Python、NumPy、scikit-learn；阅读PDF图像时按可用PDF工具处理。大篇论文分段读取，用返回的截断提示继续；全文按页保存在assets/pages，原PDF位置和哈希在assets/papers.json。

## 全文精读和独立作答要求

开展逐篇学习或测试时，读取[full-paper-study-protocol.md](references/full-paper-study-protocol.md)。用户范围已升级为全文及附录，图表数量/构图/论证和可运行复现分别登记；测试必须先独立完成并冻结答案，再看论文。
