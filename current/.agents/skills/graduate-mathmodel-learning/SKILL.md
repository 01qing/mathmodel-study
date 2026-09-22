---
name: graduate-mathmodel-learning
description: MathModel-Core 核心知识 Skill。面向全国研究生数学建模竞赛的长期学习、复盘、模型竞争、复现与跨题迁移。基于现有 MathModel-Skill Standard/Codex 工作流，提供深度题解、候选模型竞争、优秀论文批判性精读、数学到代码映射、风险与失效条件、独立训练、知识卡沉淀和跨会话学习状态。正式比赛模式必须交回 paper-workflow-orchestrator，禁止绕过原 S0-S8 证据链。
---

# MathModel-Core（兼容目录名：graduate-mathmodel-learning）

## 本地当前入口（2026-09-21）

本目录来自核验过的v1.41.0封存版，是后续本地工作副本。先读项目根目录 `PROJECT_STATE.json` 与 `START_HERE.md`，当前工作状态不能被下方历史版本章节覆盖。用户委托自主整理、选择案例，暂不提供个人答案；默认不要求先答练习。完整解答、学习目标与当前案例读 [本地交付导向学习](references/delivery-learning-local.md)。该说明是流程整理，尚无新增能力或获奖率提升证据。

## 1. 角色边界

本 Skill 是 `yushui2022/MathModel-Skill` 的**旁路教学层**，不是第二套正式比赛流水线。

必须复用原版能力：
- `paper-workflow-orchestrator`
- `problem-doc-model-selector`
- `modeling-paper-rubric-and-model-selector`
- `authoritative-data-harvester`
- `data-cleaning-and-visualization`
- `model-code-and-result-generator`
- `quality-assurance-auditor`
- `paper-formal-writer`
- `paper-micro-unit-generator`
- `context-memory-keeper`

禁止：
1. 重写 S0-S8 正式阶段。
2. 伪造 `run_manifest.json`、`evidence_gate_report.json` 或 `format_check_report.json` 的 PASS。
3. 将学习资料或优秀论文作者主张直接当作正式运行证据。
4. 把学习状态塞入 `paper_output/context/workflow_memory.json`。
5. 因为模型更复杂就默认更适合竞赛。

开始复杂任务前先读：
- `references/architecture-boundary.md`
- 当前模式对应的 reference
- `learning_output/context/learning_state.json`（若存在）

## 2. 五种模式

### learn
用于系统学习一道题、某一问或一种方法。

必须覆盖：
- 题目真正要求什么
- 自然语言如何变成数学结构
- 数据字段如何映射到变量
- 目标、约束、假设
- 至少 3 条候选路线：最小基线、推荐主方案、合理替代
- 为什么选主方案
- 为什么不选其它方案
- 什么条件下应改选
- 公式来源与推导
- 数学 → 算法 → 代码 → 结果
- 验证
- 风险与失效条件
- 可迁移总结

若原版已有 `problem_analysis.json` / `model_route.json`，优先读取，不重复建立第二套真相源。

### competition
正式完成比赛题。

必须立即回到 `$paper-workflow-orchestrator`，严格按 S0-S8 执行。
本 Skill 只允许生成旁路学习记录，不得接管正式 PASS 状态。

### paper-review
精读一篇或多篇优秀论文。

必须逐问区分：
- 作者事实
- 作者主张
- 已核验
- 部分核验
- 未核验
- 与证据矛盾
- 我们的推断

不得只做摘要。多论文比较必须按同一子问题横向比较。

### review
赛后或学后复盘。

重点抽取：
- 哪个判断正确
- 哪条路线浪费时间
- 哪个假设最危险
- 哪种错误具有可迁移性
- 下次如何更快识别

应更新 `knowledge_base/error_patterns/` 或 `competition_lessons/`。

### practice
独立做题训练。

必须先让学习者独立提交：
- 问题结构
- 变量、目标、约束
- 候选模型
- 推荐方案
- 验证方案

然后再对照：
- 学习者方案
- 优秀论文方案
- 原 MathModel 正式路线（若有）
- 综合判断

禁止在训练开始就泄露完整标准方案。

## 3. 模型竞争规则

读取 `references/candidate-model-competition.md`。

每问至少保留：
1. 最小可用基线
2. 推荐主方案
3. 一个真正合理的替代方案

比较维度至少包括：
- 问题结构匹配
- 数据要求
- 假设强弱
- 可解释性
- 精度潜力
- 样本风险
- 调参成本
- 实现难度
- 竞赛时间风险
- 验证难度
- 创新空间

必须明确给出：
- 当前倾向
- 排除理由
- 切换条件

禁止用“各有优缺点”结束模型比较。

## 4. 优秀论文证据规则

读取：
- `references/paper-review-protocol.md`
- `references/evidence-and-verification.md`
- `references/code-paper-figure-learning.md`
- `references/dev-casegroup-contracts-v141.md`

统一状态：
`author_claim | verified | partially_verified | not_verified | contradicted | our_inference`

代码未实际运行，不得将其数值结果或完整复现标记为 `verified`。静态数据流或公式核验可以记录具体发现，但必须标明核验范围，不能推广为整体代码正确。
论文自报奖项未从可信来源核验时，不得写成已核验奖项。

## 4.1 代码、图表与论文联合学习

当资料包含作者/教师代码、附录代码、结果图或结果表时，必须读取 `references/code-paper-figure-learning.md`。

最低要求：
- 论文与代码分开登记来源和 SHA；
- 先静态审计，再做最小可运行验证；
- 建立“子问→公式/步骤→代码文件/函数→输出图表→结论”映射；
- 图表记录构图、证据作用和不能证明的内容；
- 代码只通过语法检查不得称为已复现；
- 教师/专家资料可用于训练规则和案例，但不能冒充优秀论文或官方答案。

通用静态审计入口：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/audit_code_bundle.py \
  <code_root> --output learning_output/analyses/<case>_code_audit.json
```

相似新题命中已审计案例时，应把具体可复用代码阶段、图表证据结构、已知 bug 和最小验证实验一起交给 `mathmodel-case-retriever`。

### 4.2 同题多论文横向学习

当同一赛题存在多篇优秀论文时，不能只生成三份独立摘要。必须按子问形成：

`共同任务 → 各论文路线差异 → 最小基线 → 主方案选择条件 → 代码映射 → 图表论证 → 风险/放弃条件`。

2025 E 当前训练映射先读：
- `references/2025-E-cross-paper-code-figure-map.md`
- `knowledge_base/cross_paper_maps/2025-E-S039-S041-with-code.json`

新题若仅局部相似，必须精确到 Q1/Q2/Q3/Q4 或更细步骤，不得因为“都是迁移学习”就判为整题相似。


## 5. 长期学习状态

学习状态保存在：

`learning_output/context/learning_state.json`

掌握等级：
- `unseen`
- `introduced`
- `can_explain`
- `can_apply_with_help`
- `can_apply_independently`
- `can_compare_and_adapt`

升级要求见 `references/memory-and-recovery.md`。

新对话恢复时：
1. 读 `learning_state.json`
2. 读 `next_learning.md`
3. 若当前任务同时属于正式比赛，再读原 `workflow_memory.json` 和 workflow guard
4. 以文件状态为准，不依赖聊天历史猜进度

## 6. 目录边界

只允许本 Skill 主动维护：

```text
learning_sources/
learning_output/
knowledge_base/
```

原版目录：

```text
problem_files/
crawled_data/
paper_output/
```

必须遵守原 MathModel-Skill 的所有权和正式契约。

## 7. 数据契约

本 Skill 的学习状态、来源索引、方法卡、题型卡、论文复盘卡和 session 记录均配有 `schemas/` JSON Schema。结构化写入时优先遵守 schema，避免跨对话后字段漂移。

## 8. 初始化

从项目根目录运行：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/init_learning_workspace.py
python .agents/skills/graduate-mathmodel-learning/scripts/validate_learning_workspace.py
```

## 9. 资料入库

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/index_learning_source.py \
  --path-or-url "<path-or-url>" \
  --source-type excellent_paper \
  --year 2023 \
  --problem-id A
```

资料入库只建立索引，不自动宣称内容正确。

## 10. 更新学习状态

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/update_learning_state.py \
  --mode learn \
  --year 2023 \
  --problem-id A \
  --next-action "逐问比较两篇优秀论文"
```

方法掌握度必须有证据：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/update_learning_state.py \
  --method xgboost \
  --method-level can_explain \
  --method-evidence "session:2023A-q1-review"
```

## 11. 知识卡

用：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/create_knowledge_card.py \
  --type method \
  --id xgboost
```

生成模板后由 Agent 根据真实学习证据填写。
不得用空模板冒充已掌握知识。

## 12. 校验

完成重要学习阶段后运行：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/validate_learning_workspace.py
```

若正式比赛产物参与本轮分析，学习报告必须注明其当前正式状态，不能把旧/过期 contract 当作 fresh evidence。

## 12. 研赛资料目录与案例 Manifest

长期资料治理必须读取：

- `references/source-governance.md`
- `assets/catalog/source_catalog_2021_2025.json`

校验：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/validate_source_catalog.py
```

开始一套真实案例前先创建 case workspace：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/validate_case_manifest.py
python .agents/skills/graduate-mathmodel-learning/scripts/build_case_workspace.py
```

默认首个验收案例为 `gmcm-2021-D`。其题名存在公开来源冲突，因此不得静默把“胰腺癌/乳腺癌”统一为某一个词；应先依据题面正文、变量和数据语义核对，并把结论记录在案例 metadata 中。

大型原题、Excel 和论文 PDF 不进入 Skill 安装目录，应落到：

`learning_sources/competitions/<year>/<problem_id>/`

## 13. 真实案例的论文筛选与 Blind Baseline

2021 D 的首组论文对照读取：

- `references/paper-screening-2021-D.md`

但正式 `learn` 验收时不得把该文件作为输入证据。应在隔离会话中读取：

- `references/blind-baseline-2021-D.md`

并只提供题面与附件。

核心原则：

1. 论文筛选 Agent 与 blind-solve Agent 应逻辑隔离；
2. 优秀论文的算法名不能成为模型选择先验；
3. Q3 类别不均衡时禁止只报告 Accuracy；
4. 任何过采样必须发生在训练折内部；
5. Q4 必须先审查描述符空间的可行性与真实分子可实现性，再讨论 PSO/GA/NSGA 等求解器。

## 14. Fresh Blind Eval 隔离

当前研发会话已经读过优秀论文时，禁止把同一会话后续解答标为 `fresh_blind`。

先生成隔离包：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/prepare_blind_eval.py
python .agents/skills/graduate-mathmodel-learning/scripts/validate_blind_bundle.py
```

然后在**新会话/隔离上下文**只读取：

- `learning_output/blind_eval/gmcm-2021-D/problem_facts.json`
- 题面
- 原始4个附件
- 通用学习 Skill 规则

禁止读取：
- 优秀论文
- `paper-screening-2021-D.md`
- `reference-baseline-2021-D.md`

2021 D 的 Q4 额外硬约束：
- Caco-2 favorable = 1
- HOB favorable = 1
- hERG favorable = 0
- MN favorable = 0
- CYP3A4 favorable 方向不得静默假定，必须声明约定或做敏感性分析。

## 15. 数据审计门禁

2021 D 在正式选模和代码基准前必须先运行：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/audit_2021_D_data.py \
  --data-dir learning_sources/competitions/2021/D/data
```

必须读取 `references/2021-D-data-audit-gate.md`。

若当前环境只能确认 GitHub 二进制文件存在、但没有真正取得 XLSX 内容：
状态必须保持 `READY_AWAITING_BINARY_FILES`，禁止用题面数字冒充实际数据统计。

## 16. Leakage-Safe Model Benchmark

数据审计状态为 `PASS` 或 `PASS_WITH_WARNINGS` 后，读取：

- `references/leakage-safe-model-benchmark.md`

正式运行：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/benchmark_2021_D_models.py \
  --data-dir learning_sources/competitions/2021/D/data \
  --profile standard
```

校验：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/validate_model_benchmark.py
```

硬约束：

1. Q1 特征选择必须位于每个 CV 训练折内部；
2. Q2 比较的是完整 `selector + regressor` Pipeline；
3. 所有候选共享同一 outer folds；
4. Q3 五个标签独立竞争模型；
5. Accuracy 不能成为 Q3 唯一或首要模型选择指标；
6. 官方 test 50 条完全不参与 benchmark；
7. Top2 practical tie 时优先推荐更简单、更稳的路线；
8. `decision_explanations` 必须说明推荐理由、runner-up 和 switch condition；
9. benchmark 只证明“在声明的验证协议下更优”，不得声称某算法普遍最优。

## 17. Final Fit 与官方 Test 预测

只有 benchmark contract 校验通过后，读取：

- `references/final-fit-and-test-prediction.md`

运行：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/finalize_2021_D_models.py \
  --data-dir learning_sources/competitions/2021/D/data
```

校验：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/validate_final_fit.py
```

硬约束：

1. model family 与 selector family 必须来自已冻结 benchmark；
2. final-fit 超参数只能使用训练数据内部 CV；
3. test 50 条只允许最终一次预测；
4. 不允许因 test 预测“看起来不好”而回头换模型；
5. Q2 保存最终 Top20、pIC50 与反算 IC50；
6. Q3 每个标签保存最终类别和可用时的概率。

## 18. Paper-vs-Benchmark Comparison

准备结构化对照：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/prepare_paper_benchmark_comparison.py
```

读取：

- `references/paper-vs-benchmark-comparison.md`

程序只负责生成证据包，不自动完成“哪篇更好”的判断。

Agent 必须逐问填写：
- paper A strengths
- paper B strengths
- our strengths
- our weaknesses
- adopt
- do not copy blindly
- preferred learning source
- confidence

未完成 Agent Review 时禁止知识抽取。

## 19. Case Knowledge Extraction

读取：

- `references/case-knowledge-extraction.md`

只有论文对照已经完成并将 `agent_review_required=false` 后，才运行：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/extract_case_knowledge.py
```

知识卡必须保留：
- evidence status
- source case
- applicability
- failure conditions

阅读优秀论文本身不能把掌握等级直接升级为 `can_apply_independently`。

## 20. External Modeling Code Audit

学习优秀论文或公开参赛代码时，必须读取：

- `references/external-modeling-code-audit.md`

若代码已经落盘，可先静态扫描：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/scan_ml_code_risks.py \
  --root <code-directory>
```

静态扫描只是候选风险，不等于最终判断。Agent 仍需检查完整数据链和上下文。

2021 D 已有一个真实公开代码审计资产：

```text
assets/cases/2021_D_external_code_audit.json
```

其作用不是证明“这个队伍做错了”，而是训练以下能力：

1. 区分论文思路与代码实现；
2. 找出 preprocessing / feature selection / PCA / resampling 的 fit 边界；
3. 检查 validation/test 是否被反复用于选模；
4. 检查最终 test 是否错误地重新 fit scaler/PCA；
5. 检查 metric API 的 `y_true, y_pred` 顺序；
6. 同时记录值得学习的实现思路，不做只挑错误的审查；
7. 上游代码链缺失时使用 `unresolved`，禁止猜测。

真实代码中的数值结果只有在运行环境和数据都复现后才可以升级为 `verified`。

## 21. 2021 D Source Acquisition 与镜像交叉核验

真实案例运行前读取：

- `references/2021-D-source-acquisition-and-crosscheck.md`

资料角色必须区分：

- `zhanwen/MathModel` XLSX：`contest_attachment_mirror`
- `Bureaux-Tao/modeling2021-D` CSV：`participant_converted_mirror`

远程存在不等于本地已审计。

在有网络的 Codex / 本地环境中：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/acquire_2021_D_sources.py \
  --source both

python .agents/skills/graduate-mathmodel-learning/scripts/verify_2021_D_sources.py
```

然后分别审计：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/audit_2021_D_data.py \
  --data-dir learning_sources/competitions/2021/D/xlsx

python .agents/skills/graduate-mathmodel-learning/scripts/audit_2021_D_csv_mirror.py \
  --csv-root learning_sources/competitions/2021/D/csv_mirror
```

CSV 只有在以下命令返回 `CROSSCHECK_PASS` 后，才允许代替 XLSX 进入真实 benchmark：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/crosscheck_2021_D_xlsx_csv.py \
  --xlsx-root learning_sources/competitions/2021/D/xlsx \
  --csv-root learning_sources/competitions/2021/D/csv_mirror
```

硬约束：

1. 获取后必须核验 byte size + Git blob SHA-1；
2. CSV 与 XLSX 必须核对 train/test 行数、SMILES、列名、标签和数值；
3. participant CSV 未经交叉核验时只能用于代码理解，不能升级为 primary modeling input；
4. 当前环境网络受限时，状态保持 `NETWORK_BLOCKED` / `REMOTE_METADATA_CONFIRMED`，禁止写成真实数据审计通过。

## 21. 第二迁移案例：2024 C

为避免 Skill 只对 2021 D 的表格机器学习结构过拟合，第二案例固定为：

`gmcm-2024-C 数据驱动下磁性元件的磁芯损耗建模`

开始前读取：

- `assets/cases/2024_C_problem_facts.json`
- `assets/cases/2024_C_case_manifest.json`
- `references/2024-C-learning-route.md`
- `references/cross-case-transfer-2021D-2024C.md`

创建学习目录：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/build_learning_case.py \
  --manifest .agents/skills/graduate-mathmodel-learning/assets/cases/2024_C_case_manifest.json
```

2024 C 专属硬约束：

1. Q1 先解决波形表示，再选分类器；1024点不能无解释地当1024个普通独立变量；
2. Q2 必须保留 Steinmetz 物理基线与温度修正的可解释性，黑箱回归只能做比较；
3. Q2 至少做逐温度误差或留一温度验证，不能只报随机CV；
4. Q3 分析温度、波形、材料时必须控制频率与磁通密度峰值等重要协变量；
5. Q3 必须区分 p-value 与效应大小；
6. Q4 需检查跨温度/材料/波形工况泛化，不能只靠随机K折；
7. Q5 优先输出 Pareto trade-off；加权和只能作为偏好选择，不得无依据地产生唯一“最优点”；
8. Q5 surrogate 优化必须受数据支持域/模型适用域约束。

## 22. 2024 C 真实代码审计与论文门禁

第二案例继续时必须读取：

- `references/2024-C-code-audit.md`
- `assets/cases/2024_C_external_code_audit.json`
- `references/2024-C-paper-screening.md`
- `assets/cases/2024_C_paper_screening.json`

核心规则：

1. Q1 随机 holdout 的 `Accuracy=1.0` 不能直接升级为跨工况泛化结论；
2. 波形统计特征必须从不可变的原始1024点矩阵计算，避免派生特征污染后续统计量；
3. Q2 温度修正项不能只靠边际 `P vs T` 关系选择，必须控制 `f` 与 `Bm`；
4. Q2 至少增加逐温度/留一温度验证；
5. Q3 当前代码体不可读，相关实现保持 `unresolved`，禁止根据图片文件名推断方法；
6. Q4 预测参数和物理参数必须区分“可校准”与“可识别”；
7. Q4 必须给出与跨工况泛化相匹配的验证协议；
8. Q5 每个题面目标都必须在 objective contract 中出现；
9. 已核验的 Tereaslle Q5 只最小化磁芯损耗，没有编码 `maximize f*Bm`，因此不能视为完成题目双目标优化；
10. 2024 C 的两篇优秀论文仍未 materialize，冠军新闻稿只能作为 solution profile，不能当全文论文使用。

## 23. Blind 顺序门禁与 2024 C 独立模型竞争

### 23.1 2024 C 状态修正

2024 C 在候选模型矩阵冻结前已经读过公开代码和获奖方案，因此：

`fresh_blind = false`

只能使用：

`RETROSPECTIVE_INDEPENDENT_ROUTE_NOT_FRESH_BLIND`

读取：

- `assets/cases/2024_C_blind_contamination.json`
- `assets/cases/2024_C_independent_model_competition.json`
- `references/2024-C-independent-model-competition.md`
- `references/blind-contamination-and-ordering.md`

### 23.2 新赛题的强制顺序

以后首次学习一个未接触赛题时：

1. 只允许题目正文和官方附件；
2. 先创建 blind gate；
3. 完成 L1-L4 和候选模型竞争；
4. 冻结矩阵并写入 hash；
5. 然后才允许读取优秀论文、代码、博客、获奖方案。

初始化：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/start_blind_case.py \
  --case-id <case-id> \
  --problem-fingerprint <hash>
```

冻结：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/freeze_blind_matrix.py \
  --gate <gate.json> \
  --matrix <matrix.json>
```

只要在冻结前已经读取任何解法，永远不能再把该案例标成 fresh blind。

### 23.3 2024 C 独立推荐主线

- Q1：不可变原始波形 -> 时间域/斜率/频域特征 -> RF/SVM；1D CNN 仅作升级候选。
- Q2：原 Steinmetz -> 可解释温度修正；用 leave-one-temperature-out 选择复杂度。
- Q3：控制 `log f`、`log Bm` 的 ANCOVA/稳健回归 + 三主效应 + 三个两两交互 + 效应量。
- Q4：物理基线 + Ridge + 树模型 + boosting 同台；随机CV与跨工况验证分开报告。
- Q5：显式 `min P_hat` 与 `max f*Bm`；优先 Pareto/NSGA-II 或 ε-constraint，禁止漏目标。



## 24. v1.6：在v1.5上继续改进
本版本保留原五模式和正式S0–S8边界。最新本地资料清单为assets/catalog/local_papers_2024_2025.json；第22节的“尚未取得论文”仅描述v1.5历史，不覆盖这个新清单。核验用scripts/validate_paper_inventory.py --manifest <清单>。
2025 E学习时读取assets/cases/2025_E_case_manifest.json、2025_E_external_code_audit.json、2025_E_paper_review_partial.json及references/2025-E-evidence-lessons.md。本案例已接触解法，不能称盲测；实际只完成派生特征诊断及局部代码/论文复核。
参考特征对照用scripts/benchmark_2025_E_reference_features.py <CSV> <输出JSON>，输出写learning_output/analyses/，不作为原版model_benchmark或正式S6 PASS。
本次用户主要要求改善Agent方法库：默认不强迫用户先答练习题，不因读过论文升级用户掌握度。用户明确练习时才启用practice的先答后反馈。
盲测初始化保留旧污染状态，冻结相同矩阵幂等、不同矩阵拒绝覆盖。它保护正常脚本流程，不能阻止手工删改或证明模型没有先验接触。旧题重新开会话不能自动恢复盲测资格。

## v1.7开发中的局部相似论文检索

用户询问新题像哪年哪题，或需要跨题寻找可迁移方法时，使用同项目的`../mathmodel-case-retriever/SKILL.md`。先保存题目事实，按子问返回原文页码、相似结构、差异及最小验证，再回到本Skill的模型竞争流程。45篇全文索引已建立，逐篇正文评审尚在进行；不能把检索功能可用或完整索引称为45篇已学完。评估模式只使用训练组库；生产模式可使用全库，两者分开报告。
## 正文—代码—结果一致性闸门

对带附录代码的训练论文，不能只验证“代码存在”。至少检查：

1. 正文数据划分与代码划分是否一致，尤其是时间、原文件、设备、病例等分组边界。
2. 正文模型公式与代码目标函数/损失函数是否同一个量。
3. 物理常数、单位和约束在不同脚本中是否一致。
4. 多目标优化是否声明 Pareto 集到最终运行点的选择规则。
5. 图表证明的是聚合约束还是逐对象约束；不能用前者代替后者。
6. 对表格可复算的百分比、均值、比值做自动算术复核。
7. 任何名为 SNR、R2、MAPE、置信度等指标都要核对代码实现与数学定义。



## v1.11：复杂算法名称的实现证据门禁

学习 2024-A S003 时读取：

- `references/2024-A-S003-paper-code-audit.md`
- `knowledge_base/paper_reviews/2024-A-S003-core.json`
- `knowledge_base/code_cases/2024-A-S003-appendix-code.json`
- `knowledge_base/cross_paper_maps/2024-A-S001-S003.json`

新增硬规则：

1. 摘要、正文、附录的方法名必须交叉核对；“网格搜索/随机搜索”等不能混写。
2. 自适应、MPC、Pareto、鲁棒、Kalman、PSO 等名称必须能映射到实际代码路径；仅流程图出现不算实现证据。
3. SciPy `type=ineq` 统一按 `g(x)>=0` 审核，并自动做边界/内点/外点三类约束单元测试。
4. 物理模型和标准化特征必须分离量纲；标准化变量未经反变换不能直接进入有单位的物理定律。
5. MPC实现至少检查：状态或预测模型、有限时域决策、跨时刻动态/变化率约束、滚动只执行第一步。缺任何关键项时降级描述为静态/滚动近似，禁止只按论文标签命名。
6. 多目标优化若声称Pareto，论文图表必须给实际前沿与最终选点；只有权重文字没有前沿证据时标记 evidence gap。
7. 鲁棒性至少做噪声/延迟严重度扫描；单个受扰数据集只能说明该工况表现。
8. 打印附录不完整时，结论表述为“可见打印代码未实现/未展示”，不得扩大成“完整提交代码一定没有”。

## v1.12：独立实体状态、多指标与校准证据门禁

学习论文或生成新方案时增加以下强制检查：

1. **独立实体状态重置**：Kalman、RNN 隐状态、递推估计器、在线统计量若用于多台设备/多患者/多站点，默认必须在实体边界重置。除非论文明确建模共享状态，否则跨实体继承属于数据/状态泄漏。
2. **局部窗口循环复用**：高度重叠滑窗的局部幅值不能自动当作每秒新发生的完整疲劳循环。若窗口输出被累加为损伤，必须和精确雨流在已知循环信号上做重复计数、尺度和边界测试。
3. **物理参数语义**：不仅检查单位，还检查参数定义是否属于正确物理过程。功率因子、机械效率、发电机效率、空气动力系数等不得因“数值范围合适”互相替代。
4. **校准—评价分离**：固定偏移、时滞、阈值、修正系数、Q/R、经验常数只要通过数据拟合选出，就属于模型训练/校准，必须在独立时间块、实体或场景上评价。
5. **优化器目标函数证据**：看到 GA/PSO/DE 等顶层框架不等于目标函数已实现。必须定位 `objective/evaluation/fitness` 的实际计算以及约束处理；附录缺函数时标记为不可复现。
6. **归一化后再验约束**：把权重归一化满足和为1，可能再次破坏每个分量的上下界。所有投影/归一化/修复操作之后必须重新执行逐实体可行性检查。
7. **多指标不做“全面胜利”偷换**：先标明每个指标“越大越好/越小越好”，若存在一项明显恶化，就描述为权衡并给 Pareto/效用选择规则，不得笼统写“综合最优”或“所有指标显著优势”。
8. **实时性分清吞吐量和延迟**：整批100/2000个时间点的总运行时间、平均每步时间和线上单步 p95/p99/max latency 是不同证据。实时约束以单步最坏/高分位延迟和硬件环境为主。
9. **处理组标签锁定**：消融/对照方式一旦在表格定义，后文、图例、代码枚举必须使用同一ID→处理映射；发现方式2/方式3互换时，不允许继续做结论汇总。


## v1.13：WLAN实验组、功率量纲与回归指标门禁

学习 2024-B S005 时增加以下强制检查：

1. **先定义独立样本单位再切分**：同一实验、设备、会话、患者、轨迹或原始文件产生的多行/多窗口默认属于同一 group；禁止先按行随机切分再声称泛化。
2. **预处理只在训练组拟合**：插补、标准化、特征选择、降维、阈值调参全部在 split 之后 fit；验证/测试只 transform。
3. **dBm 先回线性功率域**：RSSI、干扰、噪声的功率求和必须在 mW/W 域完成，SINR 比值计算后再转 dB。
4. **中间量到标签先查可识别性**：若先预测 PHY Rate 再映射 (MCS,NSS)，必须验证映射是否单射；存在碰撞时不得把标量预测准确等同于标签准确。
5. **回归不用无定义“准确率”**：连续目标默认报告 MAE/RMSE/R2（适用时）以及绝对/相对误差 P50/P90/P95 和明确容差覆盖率。
6. **损失函数输入契约检查**：例如 PyTorch CrossEntropyLoss 输入应为 logits；若模型 forward 已 softmax，必须修正或证明所用损失接受概率。
7. **特征重要性不自动等于因果影响率**：RF/GBDT/SHAP/Permutation importance 默认表述为预测重要性，并检查跨 group fold 稳定性。
8. **论文声明的算法改进必须定位实现证据**：如“按每棵树误差加权随机森林”“残差连接优化 CNN”，需定位实际代码；打印附录未展示时标记 evidence gap，不得自动视为已实现。


## v1.14：过采样、目标编码与级联模型 OOF 门禁

学习 2024-B S006 时增加：

1. **目标编码必须 split-first + cross-fit**：TargetEncoder/类别均值编码不能在全体样本上用 y 拟合后再切分；训练行优先用 out-of-fold 编码。
2. **过采样只在训练折内**：RandomOverSampler、SMOTE、ADASYN 等不得在全数据上扩增后再切分；验证/测试必须保持原分布。
3. **重采样 API/张量形状先烟测**：表格重采样器通常要求二维 X 和一维类别 y；CNN reshape/one-hot 应在安全的重采样顺序之后完成。
4. **级联/stacking 用 OOF 中间预测**：若线上第二层接收第一层预测量，则第二层训练也应使用第一层的 out-of-fold 预测，不能用真实中间量替代。
5. **必须报告端到端级联指标**：第一层和第二层单独高分不能替代完整链路评估；要在 untouched group 上跑全链并分析误差传播。
6. **随机噪声加在最终预测上不等于鲁棒训练**：没有训练时扰动、鲁棒目标或概率模型时，不得把 post-hoc output noise 写成“提高泛化/鲁棒性”。
7. **无固定随机种子的提交输出不可复现**：最终预测中的随机选择/高斯扰动必须有明确统计模型与 seed/重复运行证据，否则删除。
8. **同题方法比较允许局部借鉴**：S006 的“直接联合预测 (MCS,NSS)”可以优于 S005 的 PHY Rate 反演思路；但其验证泄漏不能随方法一起照搬。

## v1.15：结构化标签、类别不平衡与跨章节指标一致性门禁

学习 2024-B S007 时增加：

1. **结构化标签不能只看边际准确率**：MCS/NSS、部件/状态、地区/等级等有合法组合约束的多输出，若用独立分类器预测，必须验证重组后的 tuple 是否属于合法/训练支持集合；优先联合类别或约束解码，并报告 joint exact-match 与 invalid-pair rate。
2. **高 Accuracy + 低 F1 是类别不平衡警报**：当 Accuracy 接近 1 而 macro/per-class F1、Precision、Recall 明显偏低，禁止写“数据更平衡/模型容易”；必须看 support、混淆矩阵、macro F1、balanced accuracy 和少数类召回。
3. **dBm/RSSI 聚合回线性功率域**：SINR、多个干扰源、多个天线功率的求和默认先做 `mW = 10^(dBm/10)`（或等价 W 公式），完成物理聚合后再转回 dBm。直接在 dBm 上相加不代表功率和；算术平均也必须说明其统计而非功率语义。
4. **摘要—表格—正文—代码四方结果对齐**：核心 MSE/MAE/MAPE/F1/收益率等建立单一 machine-readable result registry；论文导出前自动检查四处值是否一致。不同问题出现完全相同指标时必须复核是否复制错误。
5. **自定义“精度”必须命名清楚**：例如 `1 - P90(|relative error|)` 是任务自定义 precision score，不是标准 regression accuracy。正文优先直接报告 P50/P90/P95 误差和容差覆盖率。
6. **模型数量/方法名跨章节一致**：摘要说“8种模型”、正文结果实际“9种模型”时视为论文一致性缺陷；最终提交由方法清单 registry 自动生成摘要/正文枚举。
7. **物理公式与文字方向一致**：AMC、阈值策略等若公式表示高 SINR 允许更高 MCS，而文字却写成相反方向，必须通过单调性/边界单元测试决定正确版本，不能同时保留。
8. **同题横向借鉴取长不取漏**：S007 的 SINR 线性功率实现优于 S005/S006 的错误 dBm 算术；S006 的联合 `(MCS,NSS)` 类别结构又优于 S007 无约束独立头。新方案应组合两者优点，而不是整篇照搬。

## v1.16：真实序列、指标代数与物理基线门禁

学习 2024-B S008 后增加：

1. **LSTM/RNN 必须有真实序列轴**：把独立表格样本 reshape 为 `(n,1,p)` 只有一个 timestep，不能作为“长期依赖/时序记忆”证据。使用循环模型前必须定义实体/会话内顺序、窗口长度 `T>1`，并和同特征的 MLP/树模型做消融。
2. **核心指标自动做代数可行性检查**：同一误差集合必须满足 `MSE >= MAE^2`、`RMSE=sqrt(MSE)`；比例/概率在合法范围内；混淆矩阵可重算 Accuracy/Precision/Recall/F1。违反恒等式的表格不得进入终稿。
3. **存在机理公式先建物理基线**：如 WLAN 吞吐量可用 `PHYRate*(1-PER)*(seq_time/test_dur)` 近似时，先把它作为基线；黑箱 ML 只在 untouched group 上稳定改善后才保留，优先考虑残差建模。
4. **多干扰功率禁止连续减 dBm**：多个干扰源必须各自转线性功率求和后进入 SINR；`rssi_signal-rssi_i-rssi_j` 不是多干扰 SINR。
5. **非单射逆映射再次硬化**：PHY Rate 表中存在重复速率时，排序后“取不超过预测值的最后一项”只是代码顺序决策，不是可识别的 `(MCS,NSS)`。默认改为联合合法标签/候选集合+约束解码。
6. **上游预测进入下游时必须部署一致**：Q1/Q2 的预测量如果是 Q3 测试输入，则 Q3 训练也用 OOF 上游预测，不能用真实 seq_time/PHY 等 oracle 中间量替代。
7. **模型选优必须和自己的表格一致**：若某表数值暗示另一模型更优，先通过指标重算/原输出确定哪一个数值错误，未解决前不得写“最优模型”。
8. **2024-B 四篇已形成组合路线**：Q2 优先采用 S007 的线性功率 SINR + S006 的联合标签结构 + S005/S006/S007/S008 共同修正后的 group-aware/train-only 验证；不整篇照搬任何一篇。

## v1.17：特征契约、协变量调整、参数注册与优化可行性门禁

学习 2024-C S009 后增加：

1. **特征提取—训练—推理必须共用一个 schema**：特征名、顺序、单位、变换、来源列均写入 machine-readable contract。论文列出的特征、训练矩阵和提交预测矩阵必须自动比对；`X` 未定义、训练/推理特征不同或某材料单独提取后混称全数据时，直接判为不可复现。
2. **因素分析先处理连续协变量混杂**：温度/材料/波形等分类因素若与频率、幅值、剂量、基线严重程度等连续驱动量共同变化，禁止只对原始响应做 ANOVA 后把 p 值写成“影响程度”。优先 ANCOVA/稳健回归，报告调整后效应、效应量与置信区间。
3. **p 值不是影响大小**：显著性回答“与零差异是否相容”，不直接等于工程影响程度。排序因素时同时给效应量、调整均值/对比和实际量纲差异。
4. **拟合参数只允许单一 registry**：方程、正文、参数表、预测脚本和优化器从同一 JSON/CSV/对象读取参数，禁止手工重复录入。指数、科学计数法、符号和小数位漂移在论文导出前自动阻断。
5. **泛化必须有未参与拟合的条件**：同一数据拟合后得到的 R2/MAPE/残差只能叫 calibration/in-sample fit；跨材料/温度/波形/设备的泛化结论必须来自 grouped 或 leave-condition-out 验证。
6. **优化算法名必须和实现一致**：论文写 PSO/GA/NSGA-II 时必须定位粒子/种群、速度/变异/非支配排序等真实实现；`scipy.optimize.minimize` 不能自动称为 PSO。
7. **混合变量必须真的进入优化决策向量**：材料/波形等离散变量若写进数学模型，代码也必须枚举或编码这些变量。只优化连续 `f,Bm,T` 不能声称完成混合整数搜索。
8. **所有最优解必须 replay**：终稿前用“论文报告点”重新调用 exact objective/constraints，输出每个边界 slack、类别合法性、支持域距离和目标值。任一变量越界或目标无法复算，禁止写成最优解。
9. **双目标优先保留 Pareto 结构**：`P/Q`、加权和等标量化必须说明偏好与尺度。没有偏好来源时，优先枚举+非支配筛选、ε-constraint 或 NSGA-II，并展示 Pareto front 与选点规则。
10. **打印附录只作为可见实现证据**：若代码块缺中间文件、变量或完整 routing，表述为“打印代码未展示/不可完整复现”，不得假定作者完整提交一定同样缺失。

## v1.18：泛化单位、类别编码与目标尺度门禁

学习 2024-C S010 后增加：

1. **交叉验证的折必须对应真正的泛化单位**：随机行 KFold 只能证明同分布插值；若论文声称跨温度、跨材料、跨设备、跨站点、跨患者或跨会话泛化，必须按对应 group/condition 留出。`shuffle=True` 的高分不能替代 leave-condition-out。
2. **非显著不等于独立**：交互项 `p>α` 只能说明当前数据和检验未发现足够证据，不得直接写“两个因素相互独立”。需要报告交互效应估计、置信区间/等效性范围，并考虑统计功效。
3. **特征变换属于 schema contract**：不仅特征名/顺序要一致，`raw/log/standardized/normalized`、单位和 dtype 也必须一致。正文说 `log(Bm)` 而代码输入 raw `Bm` 时，直接标记 paper-code feature-transform mismatch。
4. **最佳模型必须有完整代码路径**：论文最终选“CatBoost+IGSE/stacking”等组合时，打印或源代码至少应出现该先验特征的计算、拼接、训练和预测；只展示五基本特征 CatBoost 不能视为最终模型已验证。
5. **均值指标检查 denominator**：`MSE/MAE/mean loss` 等名字必须核对是否真的除以样本数；累计平方误差直接打印为 Mean Squared Error 属于指标实现错误。
6. **1:1 数字权重不等于 1:1 偏好**：不同单位/数量级目标直接 `w1*f1+w2*f2` 时，权重先乘上了尺度效应。默认先归一化为无量纲效用，或保留 Pareto 向量，再声明决策偏好。
7. **类别编码必须锁定 vocabulary + dtype**：优化器中整数 id、中文标签、字符串标签之间转换后，必须对每个合法类别做 one-hot/embedding 单元测试；出现全零或未知类别立即阻断搜索。
8. **优化器排名要有实现与重复运行证据**：论文比较 GA/PSO/GWO 时，三者都要有实际实现、同一目标/边界/预算，并用多随机种子分布比较；只给一个 PSO 代码块不能支撑“GWO 最优”。
9. **不要用未调整的因素分析提前冻结离散决策**：Q3 的原始均值/ANOVA 若受频率、Bm 等连续变量混杂，不应先固定“最佳材料/波形”再做 Q5；至少先在完整混合变量可行域中检查 Pareto 支持。
10. **指标名称、公式和方向统一 registry**：任何名为效率、损失率、收益率的指标同时登记公式、范围、单位和越大/越小越好；`loss/(loss+benefit)` 不能一边叫效率最大化、一边按越小越优而不解释。

## v1.18：类别编码、最终特征链与目标尺度门禁

当论文把前面问题的特征、物理先验或分类结果继续传给后续回归/优化时，必须把“论文最终方案”追踪到实际代码的数据流，而不是看到变量被计算过就认为已使用。

1. **类别编码契约**：训练与推理的类别数据类型、值域、映射表、未知类别策略必须一致。所有合法类别都要通过部署编码器做单元烟测，禁止合法类别被编码成全零未知向量而不报警。
2. **计算不等于入模**：对论文声称使用的峰度、IGSE、先验预测等特征，必须追踪 `compute -> append/column -> X -> model` 完整数据流。只计算但没有加入 `X`，不得计入最终模型。
3. **最终模型身份锁定**：模型比较阶段的 baseline、增强特征模型、最终模型必须分别登记 feature schema 与参数。后续优化只能调用明确声明的部署模型，不能悄悄退回基本特征版本。
4. **变换契约一致**：正文声称 log/standardization/one-hot 等变换时，检查打印/真实代码对每个字段是否执行同一变换。尤其检查 `Bm`、温度、频率等物理量是否出现“正文取 log、代码用原值”。
5. **指标实现复算**：变量名叫 MSE 不代表实现就是 MSE。检查是否除以样本数；检查相对误差是比例还是百分数；自定义指标必须注明数值域和“越大/越小越好”。
6. **效应量优先保留**：因素分析若已经报告 effect size，这是比只给 p 值更强的证据，应保留；但仍需检查连续工况变量（如频率、Bm）是否调整，不能把抽样近似替代显式协变量控制。
7. **随机留出不自动等于泛化**：随机行切分只能证明同分布留出性能。若论文声称跨材料、跨波形、跨温度/工况通用，至少补 grouped / leave-condition-out 验证。
8. **原始尺度加权目标门禁**：不同单位/数量级目标不能因为“1:1 权重”就解释为同等偏好。优先无量纲化、归一化、Pareto 或 epsilon-constraint，并做权重敏感性分析。
9. **自定义效率指标方向检查**：例如 `loss/(loss+energy)` 实际是损耗占比，数值越小越好；名称、文字解释、排序方向必须与公式单调性一致。
10. **随机优化器公平比较**：GA/PSO/GWO 等比较必须匹配目标函数调用预算、边界和初始条件，并报告多随机种子分布。单次最好值不能证明某算法稳定更优。
11. **打印附录证据边界**：打印代码缺 GA/GWO/最终模型时，只能记录“未见实现证据”，不能反推作者原始工程必然没有；可自包含片段的烟测结果也必须标为 fragment-level evidence。

## v1.19：交互证据、架构真实性与 Pareto 可行性门禁

学习 2024-C S011 后增加：

1. **交叉均值不等于交互/协同效应**：两因素分组均值、方差、箱线图只能描述条件分布。要写“协同/交互”，必须显式估计 interaction term，并调整频率、幅值等强连续协变量，报告交互效应量与区间。
2. **标签驱动的特征筛选必须嵌套在 CV 内**：K-W、Mann-Whitney、相关性筛选、特征重要性筛选若使用标签，不能先在全体样本上筛完再做 CV/测试。100% 分类结果尤其需要 grouped/leave-condition-out stress test。
3. **模型名称必须从真实 layer graph 验证**：论文写 Bi-LSTM/attention/feature weighting/transformer 时，代码中必须能定位相应层及数据流。只出现 Conv1d+FC 时，不得把结果归因于 Bi-LSTM 的过去/未来信息学习。
4. **输入维度属于 feature contract**：正文称 10 维、代码写死 1033 维时直接阻断最终模型身份确认；每个维度来源、顺序、变换与 train/inference shape 必须可追踪。
5. **扰动鲁棒性不等于跨工况泛化**：IID 测试集加少量高斯噪声只能证明局部 perturbation robustness。跨材料/温度/设备/工况泛化必须使用相应未见 group/condition。
6. **检验统计量与 p-value 分开登记**：不得把 K-S statistic 与 0.05 直接比较后当作显著性结论。结果 registry 同时保存 statistic、p-value、alpha、assumptions 和 decision。
7. **偏好权重不得由优化器自由选择**：加权多目标中的权重代表决策偏好，应由外部指定、扫描或后验选点。把权重 `a` 放进决策向量会让优化器“优化偏好本身”，不能代表既定效用。
8. **声称归一化必须能复算**：正文说 objectives normalized 时，公式/代码必须给出 reference/min-max/scale。按公开公式复算不了表格目标值时，标记 utility contract missing。
9. **Pareto 点逐点可行性 replay**：任何 Pareto/最优解都用统一边界和 exact deployment model 重算。一个样例越界就足以说明当前结果表不能作为已验证 Pareto 集。
10. **Pareto 图“更集中”不等于更优**：NSGA-II/MOPSO 等用相同预算、多随机种子比较 hypervolume、IGD/GD、spread、可行率和运行代价；视觉集中程度只能作描述，不能作为算法优劣证据。
11. **论文有算法描述但附录无代码时保持证据边界**：记录“paper-claimed / implementation-not-visible”，可以学习思想，不能把算法排名写成代码已复现。

## v1.20：效应量、多重比较、混合变量与目标复算门禁

学习 2024-C S012 后增加：

1. **跨样本缩放必须 split/group first**：逐样本自身归一化可以在单行内部完成；但按列/特征统计的 min/max、mean/std、PCA、特征选择等必须只在训练折拟合。任何完整矩阵先算 feature-wise 极值再切分都属于验证信息泄漏。
2. **F 统计量不直接当效应大小**：ANOVA 的 F 用于检验信号相对残差的强弱，受样本量、自由度、残差方差和模型规格影响。因素排序优先 partial eta²、omega²、调整后 contrast/边际均值及置信区间。
3. **表格行/正文引用自动对齐**：正文引用 ANOVA/回归表某一行时，自动核对变量名、statistic、df、p-value。把 intercept 的 F 抄成 factor 的 F 属于终稿阻断错误。
4. **多重检验必须声明 comparison family**：多次 Mann-Whitney/t-test/相关性筛选默认执行 Holm/Bonferroni/FDR 或 global-test + corrected post-hoc；47 次逐对比较不能继续沿用未校正 alpha=0.05 后直接选“最优组”。
5. **序贯两两淘汰要做顺序不变性检查**：incumbent-vs-next 的“擂台赛”会受组排列影响。至少随机重排组顺序重复验证；更推荐全局模型/统一排名/校正后的全体 contrasts，并保留统计上不可区分的共优解。
6. **混合离散变量必须保持离散语义**：材料、波形、整数档位、枚举温度等不得仅给连续 box bound 后交给普通 GA/PSO。必须使用 mixed/integer operator、枚举、repair/round-trip decoder，并逐点检查类别词表合法性。
7. **paper/code 可行域必须来自同一 registry**：正文写 `f>=50000` 而代码写 `lb=5000` 时，优化结果一律视为未验证。变量上下界、离散集合、单位、精度全部存入 machine-readable domain registry，由公式表、优化器和 replay 共用。
8. **标量化结果表必须 exact replay**：对 `L=f1-lambda*f2` 等目标，用每行报告的 `f1/f2/lambda` 自动复算 L。只要复算不一致，就检查 lambda 标签、行顺序、单位、变换和代码版本，未解决前禁止据表选最优。
9. **扫描参数必须绑定 run config**：论文展示多个 lambda/seed/budget，而打印代码只固定其中一个值时，记录为“单配置代码证据”；完整扫描必须由外层循环或独立 run registry 生成，每行保存 exact config。
10. **随机行高分不能覆盖部署泛化**：物理+深度自表示即使随机 80/20 得到 R2≈1/MRE≈0.02，也只能叫同支持插值。跨材料/温度/波形/频率区间声明必须用对应 leave-condition-out/grouped 证据。
11. **ablation ladder 要保持验证协议不变**：DM→DMSDR→TDM→LMSE→…→WMTLMSEDSR 这种逐步改进值得学习，但只有输入 schema、split、指标、预算一致时，性能提升才能归因于新增模块。
12. **同题组合优于整篇照搬**：2024-C 的推荐路线取 S012 的物理→修正→自适应参数梯子和更完整实现证据，同时吸收 S009-S011 的参数/特征/可行性审计；拒绝任何一篇中的随机行泛化、未调整效应、域边界漂移或不可复算优化表。

## v1.21：时序窗口、物理标定与干预证据门禁

学习 2024-E S017 后增加：

1. **时序滑窗必须先划分再构造**：预测部署若面向未来时间，先按时间/日期/视频/站点划 train/validation/test，再在各自区间内生成窗口；禁止先生成高度重叠窗口后随机 `train_test_split`，否则同一时间点会跨集泄漏。必要时在边界设置 gap/embargo。
2. **时序预测图必须保留真实索引**：随机切分后的 `y_pred_train` 与 `y_pred_test` 不能简单 `concatenate` 后画回连续时间轴。每个预测值必须绑定原始 timestamp/window end index，图中明确 train/test 区间。
3. **相对代理量不得直接冒充物理量**：视频得到的“相对密度/归一化密度”若没有米/公里尺度，就不能直接代入要求 `veh/km` 的 Greenberg/Greenshields 等基本图并输出 km/h。必须先做标定、单位转换与不确定性传播；否则结果保持相对量语义。
4. **物理模型参数统一 registry**：正文写自由流速 130 km/h、代码用 `V_c=120`、又按 130 截断时视为 parameter-contract mismatch。交通基本图参数、拥堵密度、阈值和单位由同一 machine-readable registry 生成。
5. **挑两个命中案例不等于验证模型**：只检查两个预测拥堵时刻能证明“存在真阳性”，不能证明预测质量。拥堵检测/预警至少报告 event-level precision/recall/F1、false alarms/hour、miss rate、onset delay、duration error，并展示 TP/FP/FN 代表案例。
6. **相关性不推出干预效果**：监控点相关系数、同步趋势只能支撑关联/传播假设，不能直接推出“开放上游应急车道会改善速度”。干预效果需要已发生开放的数据、可信交通仿真、自然实验/因果识别或明确反事实假设。
7. **手工乘因子只能叫情景敏感性**：把速度乘 1.2/1.5/1.8/2、密度乘 0.8/0.9 得到“开放后”曲线时，若因子不是数据/仿真标定结果，只能作为 scenario/sensitivity analysis，不得写成实证改善率。
8. **状态方程先过量纲检查**：任何车流密度、流量、速度递推式先登记单位并做 dimensional sanity check；若公式计算出的量纲与变量名称不一致，禁止进入控制/优化主链。
9. **交通阈值必须有 operating-characteristic 证据**：80/60/40 km/h、15 km/h 路段速度差、连续3帧等规则若用于真实决策，应在标注事件上做阈值敏感性、ROC/PR 或成本权衡，不能只引用常识后固定。
10. **深度模型名称继续追实现证据**：论文最终选 LSTM/Transformer 等时，打印/真实代码中必须找到模型构造、sequence shape、训练、验证与推理链。只有结构示意图而无实现时标记 `paper-claimed / implementation-not-visible`。
11. **感知系统也需要端到端验证**：YOLO+DeepSORT 不能只凭代码存在就宣称车辆数准确。需要检测/跟踪计数指标、ID switch/重复计数检查、遮挡/车型分层和视频级留出验证。
12. **同题组合在完整四篇前不封死路线**：S017 只作为 2024-E 第一条路线；S018-S020 未读完前，保留其 CV→状态估计→拥堵判定→控制→布点的系统分解，但不提前宣布整题最佳方法。


## v1.22：帧时间基准、阈值状态机与优化变量契约门禁

学习 2024-E S018 后增加：

1. **帧率与时间聚合只保留一个 registry**：论文里的 FPS、每条记录帧数、秒数、代码计数器和图横轴必须由同一时间基准生成；`25帧=1秒` 与代码 `33` 帧聚合一类分叉在建模前阻断。
2. **流量与空间密度语义分离**：时间窗内通过车辆数属于流量/到达计数；只有同时占据已标定空间区间的车辆数才能直接构造 `veh/km` 密度。使用 `q≈kv` 前必须登记三个量的窗口与单位。
3. **序列模型执行图审计**：BiGRU/LSTM/attention 不按标题认定。真实 `T` 维、attention 权重变量、multi-head 结构和 forward 调用必须可追到代码；`T=1` 自动触发单时间步伪序列门禁。
4. **常用指标做代数 replay**：表格进入论文前自动检查 `RMSE²=MSE`、`MSE≥MAE²`、概率/比例边界以及混淆矩阵派生指标；发现矛盾先修结果 registry。
5. **阈值策略只有一份 Boolean/state-machine registry**：摘要、正文、代码不能分别写 OR/AND；对 15–20 m/s 一类灰区必须定义保持、滞回或第三状态，避免控制抖动和不可复现。
6. **MLE/拟合模型到业务阈值必须有证据链**：拟合分布、似然/参数、容量分位数或风险代价如何得到 0.5 veh/s 等阈值必须可回溯，不能“先拟合一个模型、再凭图取阈值”。
7. **附录代码必须回答所属子问**：问题2若宣称 Weibull/MLE 决策，附录却是 Mask-RCNN/FPN 视觉代码，只能记为不相关补充，不能提升问题2复现等级。
8. **跨站点干预响应要做 transportability 检查**：用监测点2开放数据预测监测点4开放后结果，比任意倍率更强，但仍需比较协变量、工况和效应稳定性；未验证前标为 transferred counterfactual。
9. **百分比变化统一分母**：默认 `(after-before)/before`，任何其他定义必须显式命名；所有百分比从 before/after 原值机器重算，避免增长率误用 after 作为分母。
10. **优化变量必须等于题目要决策的对象**：题目要求摄像头数量/位置时，decision vector 必须能解码出数量/位置；只优化应急车道开闭状态不能声称求得相机布点。
11. **传感器布点收益需要中介链**：布点 → 覆盖/估计误差 → 控制决策质量 → 交通结果。没有这条验证链，不把 TTT/VAV 改善归因于“加摄像头”。
12. **2024-E 当前只形成两篇 provisional 组合**：S017/S018 已精读，S019/S020 未读完前不封死整题最优路线。


## v1.23：交通量纲、库存守恒与传感器—策略依赖门禁

学习 2024-E S019 后增加：

1. **交通基本图必须时间单位闭合**：`q=rho*u` 前先检查 q 的 `veh/min`/`veh/h` 与 u 的 `km/min`/`km/h` 是否一致；所有图表、阈值、守恒方程引用同一 unit registry。
2. **展示回归式至少 replay 一行展示数据**：论文系数必须能重算表格样本到正确量级；若差几个数量级，优先检查标准化、单位、小数点、逆变换和版本抄录。
3. **提前量预测必须记录 split provenance**：10分钟/30分钟 ahead 等时间任务不能只写 70/30；保存明确的时间区间、日期/视频/站点 group、gap 与是否 shuffle。
4. **相关性/特征重要性不直接生成控制权重**：`0.4/0.6` 等策略权重必须有拟合目标、决策代价或敏感性证据；RF/AdaBoost importance 只默认视为预测性重要性。
5. **拥堵密度名称分层**：jam density、critical density、observed max density、alarm/open/close threshold 分开登记，避免 240/300/350 等数字在章节间互换语义。
6. **库存状态先审校准独立性**：`K=N/Qmax` 的 Qmax 不应由“假设 K=0.8 时刚好解除拥堵”再反推后继续用同一0.8阈值验证；容量与阈值至少有独立校准或敏感性。
7. **反事实状态方程做符号/单调性单元测试**：增加出流必须使车辆库存不升高；干预模型优先通过参数替换自动生成，避免手抄公式时 inflow/outflow 反号。
8. **固定容量提升倍率只算 scenario**：`q_out×1.3` 若没有实测开放数据/校准仿真，只能报告倍率敏感性，不把拥堵缩短百分比当作因果实证。
9. **移动/删除传感器先跑 feature dependency graph**：若策略依赖 `K_AB,K_BC` 而B摄像头被移走，必须重新定义可观测状态、训练/标定策略与阈值；不能只改布点图。
10. **附录清单不等于代码证据**：论文只列 `.py/.xlsx/.pt` 名称但未提供源文件时，复现等级保持 `manifest-only`；只有拿到源文件并通过依赖/运行/结果回放后才升级。
11. **布局建议与数值优化分开命名**：没有位置变量、可行域、成本/覆盖/控制价值目标和候选比较时，应称“启发式布置方案”，不称最优布点。
12. **S017-S019 仍是 provisional 组合**：在 S020 完成前，保留 S019 的10分钟上游预测和库存滞回结构，但最终2024-E路线不封死。


## v1.23：公式反解、回归尺度与情景干预证据门禁

学习 2024-E S019 后增加：

1. **连续编号公式必须做代数回放**：任何由 Eq.(k) “整理/反解”得到 Eq.(k+1) 的关键阈值，都用符号或至少一个数值样例回代。S019 的 `td=rhom/(rhom-rho0)*tau` 不能被反解成除以 `rho0`；反解错误直接阻断后续预警阈值。
2. **最终回归方程必须做真实行尺度烟测**：从论文数据表随机抽至少一行代入最终公式，检查预测量级、单位与目标范围。若结果相差一个数量级以上，优先排查小数点、标准化逆变换、单位或抄录错误。
3. **时间事件使用统一 registry**：拥堵开始/结束、预警时刻、持续时间在摘要、正文、表格和代码必须来自同一事件表；出现 12:56/12:57、13:24/13:26 一类漂移时先修数据源再论证模型。
4. **时序 70/30 必须声明切法**：对于分钟级序列，“70%训练/30%测试”不足以证明未来泛化；必须明确 chronological/grouped/random，并优先使用未来时间段或跨视频留出。
5. **feature importance 只作预测性解释**：上游密度高度相关时，AdaBoost/RF importance 不能直接写成“距离越近因果贡献越大”；需要 permutation/SHAP 稳定性与条件相关性分析。
6. **占有率状态需要 Q0/Qmax 校准**：`K=(Q0+∫(qin-qout)dt)/Qmax` 很适合做可解释控制状态，但 Q0/Qmax、积分步长、截断范围必须由数据/几何容量校准，并给敏感性区间。
7. **开闭阈值要有滞回且可验证**：0.8 开、0.6 关是好的 state-machine 结构，但阈值/权重必须通过历史事件、仿真或成本函数验证，不只靠距离叙述。
8. **固定 1.3 容量倍率只能叫 scenario**：手工把 `qout` 乘 1.3 得到“开放后”曲线时，48.3% 等改善率只能是该假设下的情景结果；必须做倍率敏感性，不能称实证干预效果。
9. **传感器布点必须显式优化交付量**：题目要求数量/位置/成本时，decision vector 要直接包含坐标/数量；“把 B 移到 E、再加 F”若没有坐标、成本/覆盖目标、可行域和消融，只能算启发式建议。
10. **附录只有文件清单时保持证据等级**：文件名能说明作者可能有模块化实现，但没有源码就不能审 split、参数、积分和部署逻辑；标记为 `appendix file-list evidence`，不冒充代码复现。
11. **单位阈值跨段复核**：density/flow/speed 的单位和值在所有章节统一；`veh/h` 与 `veh/km`、2700 与 300 等冲突必须在终稿前自动报警。
12. **2024-E 当前形成三篇 provisional 组合**：S017-S019 已精读，S020 未读完前仍不封死整题最终路线。


## v1.24：目标泄漏、模型自洽反事实与最差组门禁

学习 2024-E S020 后增加：

1. **特征—目标身份检查优先于训练**：在任何预测模型拟合前，对每个输入列与目标做字段身份、哈希/完全相等、确定性变换与近乎完美相关检查；目标或其副本进入 X 时，所有性能指标立即降级为无效泛化证据。
2. **预处理与时间切分顺序一起审计**：scaler/encoder/PCA/feature selection 必须在训练折拟合；面向未来的预测先 chronological/group split，再拟合预处理并构造窗口。
3. **序列模型必须证明 T>1 且时间轴有语义**：`reshape(n,1,p)` 只能说明调用了 RNN/TCN 层，不能把性能归因于长期依赖；记录 window length、forecast horizon、stride、gap 和部署时间轴。
4. **模型名称按实现原语核验**：SK-Net、attention、TCN、BiGRU 等名称必须映射到真实 branch/kernel/fuse/select/recurrent/attention 计算图；名称相似不等于结构实现。
5. **总体结论受最差组约束**：跨视频/站点/工况报告时自动保存 worst-group R²/F1/error；只要存在负 R² 或灾难性子组，摘要不得概括成“泛化能力强”而不解释失败条件。
6. **反事实状态必须回到治理模型上**：用 Greenshields/守恒/能量平衡等模型生成政策后状态时，每个 `(q,k,v)` 或状态向量重新代回同一模型；不自洽点直接拒绝进入效果比较。
7. **论文百分比从结果表机器生成**：`>70%`、`>80%`、“多数节点”等措辞从原始 numerator/denominator 重算；阈值边缘值不靠四舍五入扩大结论。
8. **情景、仿真与实证效果分级**：手工设定自由流速度、容量倍率、密度减半等只能叫 scenario；经过校准且独立验证的仿真叫 simulated counterfactual；只有真实/准实验数据才升级为 observed intervention evidence。
9. **跨领域残留终稿扫描**：交通论文出现“加料回潮设备”等无关实体时，阻断终稿并检查附近公式/模型是否也从其他模板复制。
10. **布点建议不冒充优化**：如果没有位置/数量变量、可行域、成本/覆盖/估计/控制价值目标和候选基线比较，称工程布置建议；只有显式求解并 replay 可行性后称优化。
11. **同题四篇完成后做模块级组合**：2024-E 最终路线不选“最好论文”，而组合 S019 的上游→下游提前预测和库存滞回、S020 的冲击波方向/基本图思路，并继承 S017/S018 的时序、标定、阈值和传感器证据门禁。


## v1.25：调度结果可行性、实现可见性与跨模块启发式一致性门禁

学习 2025-A S025 后增加：

1. **调度/优化结果先过硬约束 replay**：任何“最优/改进”行先检查拓扑、容量、资源独占、搬运上限等 machine-readable constraints；不可行解不得进入 Pareto 排名或摘要。
2. **同名启发式只保留一份策略 registry**：SPILL victim、priority tuple、tie-break 方向不得在 Q2/Q3/部署代码中分别实现；用同一候选集单元测试排序结果完全一致。
3. **零地址/零编号不能用 truthiness 判断有效性**：offset/id/count 允许0时统一 `is not None`/显式 validity flag，防止合法资源无法释放。
4. **强制分配必须跟可行性修复闭环**：当容量检查失败后“强制放入最大缓存”只能是临时 repair 状态；最终映射必须重新验证容量、重叠区间和 SPILL 后地址合法性。
5. **优化器名称必须追到执行主循环**：SA 要看到温度/邻域/接受准则循环；ILP 要看到变量、约束与 solver 调用；Pareto/2-opt 要看到候选生成、可行性、支配/选择循环。只有论文算法框不升级为代码已实现。
6. **图—文—表共享同一结果 registry**：收敛图的纵轴/终点、正文起止值、最终结果表必须机器一致。像 S025 图5.7 与正文数值范围不一致时阻断终稿。
7. **改进率统一一个符号和分母**：默认 improvement=(old-new)/old，减少为正、恶化为负；表格百分比从原值自动生成，不手工录入。
8. **复杂度结论绑定预算假设**：把 K/L/迭代数视为常数时必须在复杂度旁登记 fixed-budget assumption；若迭代预算随 N 扩展，重新计算渐近复杂度。
9. **跨工作负载不强求“全部改善”**：核内调度等多工作负载题优先报告 feasible rate、worst-case regret、time/transfer trade-off；允许诚实保留 Conv/Matmul 失败模式，再据此做任务自适应策略。
10. **算法图表风格学证据角色而非配色**：S025 的 Vstay 面积轨迹、峰值标记、bar+pie 配对和稀疏三线表可以借鉴；新题统一由结果 registry 生成并保持跨案例尺度可比。


## v1.25 起：MathModel-Core 统一训练协议

当前 Skill 的长期定位是 **MathModel-Core**。现阶段只训练这一份共享 Core：**不拆分、不复制知识库、不提前创建 Master / Architect / Engineer / Writer / Reviewer 角色 Skill**。未来角色化 Skill 只能共享成熟 Core，并通过接口消费知识。

从 S025 起，每个主要子问题按以下顺序学习：

`全文学习 → 代码/公式/图表审计 → Candidate Model Competition → 6小时 Baseline → 可迁移模块 → 错误模式 → Reproduction Level → 同题 Method Map → Skill 规则 → 回归测试`。

完整 case group 结束后再增加：`Mini Transfer Test`。

强制规则：
1. **Candidate Model Competition** 至少区分 Baseline、作者方案、主要替代、不推荐，并明确选择理由、排除理由与切换条件。时间序列不得因名称自动使用 LSTM；先检查真实序列轴、长度、样本量、数据量和简单模型基线。
2. **Baseline first**：回答“比赛只剩6小时最稳妥做什么”。复杂方法只有在独立验证中相对 Baseline 有稳定且实质提升才进入推荐主线。
3. **Reproduction Level R0-R7**：按 `knowledge_base/core_schema/reproduction_levels_v1.json`。视觉审查单列；没有原代码/原数据不得抬高复现等级。
4. **Same-Problem Method Competition Map**：同题多篇按 Q1/Q2/... 比较局部模块，不选“最好论文”；必须给推荐路线、稳健 Baseline、高风险高收益路线和放弃条件，并标明不能组合的接口/假设。
5. **Method Composer**：跨论文拼接前逐项检查输入输出、变量定义、数据分布、数学假设、量纲、训练/执行阶段、评价指标；存在 unknown/incompatible 不进入主线。
6. **Result Registry**：摘要、正文、表格、图片、结论不各自手录关键结果；至少复算 MSE/MAE/RMSE、R²、分类指标、百分比、目标、Pareto点、约束、参数和最优解。
7. **Figure Decision Rules**：学习图的证据任务、轴、单位、可证明与不可证明、替代图和新题使用条件；不机械复制颜色/装饰。
8. **Train/Dev/Test**：Train 学习；Dev 调规则/选模/工作流；Test 最终独立评价。Test 在独立结果冻结前禁止阅读论文答案、代码、图表、参数与结论。
9. **旧论文非破坏迁移**：S001-S020 不因 schema 升级无差别重读。旧资产原样保留，缺字段仅在方法检索/同题横向/影响决策时按需补齐。`migrate_legacy_core_cards.py` 默认只生成缺口报告，不自动改写旧卡。
10. **版本原则**：旧知识不删除、旧回归不破坏、新增知识有专项测试、版本封存后再进入下一篇。

详细协议先读：`references/mathmodel-core-v125-protocol.md`。

统一 schema：
- `knowledge_base/core_schema/mathmodel_core_question_schema_v1.json`
- `knowledge_base/core_schema/reproduction_levels_v1.json`
- `knowledge_base/core_schema/result_registry_schema_v1.json`
- `knowledge_base/core_schema/method_composer_contract_v1.json`
- `knowledge_base/core_schema/figure_decision_rule_schema_v1.json`

## v1.26：算法定义原语、同题共同评估器与多目标硬约束门禁

学习 2025-A S026 后增加：

1. **算法名称必须追到定义性原语是否真正参与更新**：例如 QPSO/ABQPSO 中的 `Mbest`、局部吸引子、量子位置更新如果只是计算后未使用，不能把普通 PSO 式更新包装成“量子粒子群已实现”。对所有复杂算法做 defining-primitives trace。
2. **禁忌表必须存“移动记录”，不能存字符流**：swap/insert/reverse 等移动用结构化 token/tuple/cell 存储，FIFO 长度按移动条目计数；禁止对拼接字符串做字符级 `ismember` 冒充禁忌判定。
3. **论文优先级公式与代码特征必须逐项对齐**：正文写 `Ptype + Psize + Pcriticality`，代码就必须能追到大小、关键度的实际计算和权重。未使用的论文特征标记为 implementation drift，并进入消融检查。
4. **主目标/次目标不能裸加不同量纲**：Bytes 与 Cycles 等不同单位若直接 `alpha*Bytes + beta*Cycles`，必须先声明归一化/偏好尺度；若题面规定一个主目标、另一个仅次要，优先使用 lexicographic 或 epsilon-constraint。
5. **最优解对象与标量 score 只保留一个真相源**：局部搜索更新 best solution 时，score、字段、收敛历史必须原子同步；禁止 `globalBest` 已改进但 `globalBestFitness` 仍旧值。
6. **跨子问同名指标必须复用同一公式 registry**：Q2/Q3 都叫“总额外数据搬运量”时，COPY_IN/SPILL 系数、单位和计数范围不得改变。Metric semantic drift 直接阻断跨问比较。
7. **硬约束先于 Pareto**：题面要求“搬运量不超过 Q2 的 1.05 倍”时，先筛可行点，再做非支配排序；把搬运量仅作为第二目标但不写硬 cap，属于模型合同缺失。
8. **同题论文比较必须先经过 common evaluator**：S025/S026 的绝对 Bytes/Cycles 只有在输入 CSV、SPILL 语义、生命周期、执行时间模拟、容量约束完全一致时才能判优。跨论文表值差异只能生成“待共同评估器复核”的候选结论。
9. **多目标论文必须画真实可行 Pareto 前沿**：通用 Pareto 示意图 + 雷达图只能解释概念/整体变化，不能证明 DPEA/NSGA-II 的非支配质量、分布均匀性或操作点选择。
10. **复杂元启发式必须和 6 小时确定性 baseline 同预算竞争**：没有稳定、实质提升就保留为高风险高收益路线，不进入 MathModel-Core 推荐主线。

### v1.27 / S027 新增 Core 决策规则

学习 2025-A S027 后增加：

1. **跨 case “平均提升”必须同时给 macro 与 aggregate/micro 口径**：若论文所谓平均值实际由总量相除得到，Result Registry 必须显式标记 aggregate-weighted，不得与每 case 百分比算术平均混称。
2. **算法名称要回落到实现原语**：Best-Fit/First-Fit、argmin/argmax spill、multi-sequence/single-case 等必须通过最小反例或符号调用图验证，不能仅信摘要名词。
3. **算法定义 helper coverage 是 R3 前置门禁**：优先级、repair、optimizer update、feasibility check 等核心 helper 只要缺定义，就最多维持 R2。代码页数多不能提高复现等级。
4. **后续问题不得手录上游 baseline**：Q3 必须通过 Result Registry/run_id 引用 Q2 的同一 baseline；若表格与代码常量漂移，所有相对改善先降级为未验证。
5. **硬约束参数单一来源**：同一 transfer tolerance 不允许正文10%、代码15%并存。先从题面/合同确定 canonical epsilon，再对每个候选 replay。
6. **多目标/权衡结论的符号由 raw before/after 自动生成**：交通/周期增加还是降低，不能手写正负号；Result Registry 自动产生 delta、ratio 和语义标签。
7. **组合式 NPU 调度的当前主线仍是 baseline first**：Q1 用确定性图调度，Q2 用生命周期/自由表 + 真正增量搬运 spill，Q3 用硬 epsilon cap 后最小 cycles；S025/S026/S027 的高级 heuristic 只有在 shared evaluator + matched budget + small exact-gap calibration 后才可晋升。



## v1.28：2025-A题组闭环与迁移验证规则

S025–S028 完成后，2025-A 的 Train case group 进入冻结状态。该题组新增以下 Core 决策规则：

1. **Q1 排序优先级必须由迁移测试校准**：合法 `FREE` 优先；其余 ready 节点先按关键路径/松弛紧迫度，再用增量内存作为 tie-break。不得把“较小 ALLOC”机械放到关键路径之前。
2. **复杂启发式必须证明 marginal gain**：SA/TS/GA/LNS/GP 等仅在同一 evaluator、相同 wall-clock/评估次数、多随机种子下稳定优于确定性 baseline 时进入主线；小实例优先以 exact enumeration / CP-SAT/MILP 校准 gap。
3. **Q2 spill 是缺口约束的子集选择，不只是单 victim 排名**：若当前需要释放 `d` 字节，局部目标应为在 `sum(size)>=d` 下最小化真实增量搬运代价。活动 victim 很少时直接枚举/DP；规模大时再用近似。
4. **Q3 hard epsilon 先于一切加权或 Pareto 排序**：先从原题唯一合同读取传输上限，过滤不可行点，再最小化 cycles；不能用权重和让一个违反硬约束但更快的点“赢”。
5. **Result Registry 必须固定 baseline provenance**：Q3 的 before 值必须用 run_id 指向 Q2 最终基线；不同表、不同算法分支或手录旧值不得混用。
6. **Pareto operating-point rule 必须可执行**：如果声明“传输优先、相同再比较时间”，代码和最终表都必须机械执行同一 lexicographic rule；图上的漂亮前沿不能替代选择合同。
7. **论文代码页数不等于复现等级**：打印附录即便很长，只要关键 helper、repair、输入数据或执行入口缺失，仍停留 R2；视觉审查继续与 R0–R7 分离。
8. **Mini Transfer Test 允许暴露 Core 自身错误**：首轮失败必须保留。修订规则后使用冻结变体确认，报告状态应写 `PASS_AFTER_RULE_REVISION`，不得把失败历史覆盖成“一次通过”。
9. **题组迁移验证不等于作者方法 R7**：Mini Transfer 验证的是 MathModel-Core 的方法选择/组合规则；除非明确迁移的是作者方法本身且成功，Paper Card 的 reproduction level 不提升。
10. **Dev 进入方式**：Train case group 完成后，Dev 不直接吸收答案。应先只暴露原题/数据，冻结独立方案，再打开 Dev paper 做规则/提示词/模型选择调优；无法获得干净 problem-only source 时，不为推进进度而提前读取 Dev 答案。

## 12. Dev/Test 检索与开发验证边界

普通 `evaluation` / `production` 检索必须限制为 **reviewed Train pages**。Dev 只能通过专门开发验证流程使用：冻结 Core → 题面/数据独立解题并冻结 → 再读 Dev 论文 → 只回写通用规则。Test 独立答案冻结前禁止读取答案、代码、图表、参数和结论。

新增通用门禁：随机行切分不等于组独立；无标签目标域分布对齐不等于准确率提升；使用目标批次统计量必须声明 transductive/batch-adaptive 部署合同；统计检验必须有实际 statistic/p-value/effect-size 证据；仅有导入缺失核心模块的 wrapper 不得升为 R3。

## 13. 能力证据与持久化版本门禁

- **Capability Evidence Gate**：规则、schema、回归测试 PASS 仅证明知识资产/合同未破坏；题组后通过 Mini Transfer 或冻结 Dev 验证证明独立解题能力。
- **Controlled Core Ablation**：重大里程碑尽量固定题目、预算、工具与评分器，对照 `No-Core / Previous-Core / New-Core`。
- **Persistent Evidence Contract**：正式版本保存修改文件、fixture、输入输出、日志、Result Registry replay、release ZIP 与 SHA256；聊天叙述不是 release 证据。
- **Lean Core + Retrieval**：SKILL.md 只保留高频决策门禁；详细论文/代码/图表/错误/结果资产仍留在同一个 Core 内按需检索。
- PASS 必须写明范围，禁止从 `regression PASS` 推导“作者算法完整复现”或“Core 能力已提升”。

## 14. 图像、几何拟合与空间决策通用门禁

1. 图像监督任务先按**原始图像/对象/采集组**切分，再切 patch/tile；像素级随机切分不是独立验证。
2. 分割指标必须记录 aggregation provenance；出现 IoU/F1 等代数关系偏差时先区分 pooled/macro/per-image，再判定错误。
3. 非线性几何拟合必须有物理参数界、残差/拟合优度和 `reject/unmodelled` 状态；算法收敛不等于物理可接受。
4. 任何样本/数据集特定校准常数必须有外部来源或 train-only 校准+held-out 验证；不得直接迁移。
5. 输出大量触及 clip 上下界时，必须报告饱和率并回看未截断量，不能据截断结果直接做相关/差异结论。
6. `histogram density` 不能直接当离散概率计算 Shannon entropy。
7. `[0,1]` 的加权兼容分数不是天然概率，未经校准应称 score/compatibility，而不是 probability。
8. 多阶段“分割→拟合→空间网络→决策”必须传播上游不确定性；若下游改用人工标注/真值中间量，必须标为 oracle upper bound，并与真实端到端结果分开。
9. 优化后的复合评分变高属于内生目标改善，不是推荐质量的独立验证；优先用 held-out outcome、反事实/仿真恢复、expected information gain 或外部效用评价。


## 15. v1.31 / S033 新增图像、拟合与主动采样门禁

1. **预测赢家与部署推荐必须分开**：若深度模型视觉/精度更强，但最终因标注、时间、算力或可解释性选传统方法，Result Registry 必须分别记录 `predictive_winner` 与 `deployment_recommendation`，并用独立指标支持二者。
2. **同一对象自拟合不是学习泛化**：一个“神经网络”若在单条曲线自身的观测上优化，再在同一曲线上报告 R²，本质属于参数化优化/曲线拟合证据；没有独立裂隙/钻孔 holdout，不得宣称跨对象学习能力。
3. **聚类组件数必须与结果实例数闭合**：代码固定 `n_components=K` 时，结果中的裂隙/对象数量必须能由该 K 产生；若数量未知，必须真正启用 BIC/AIC/HDBSCAN/拓扑实例提取等选择机制，不能只保留未调用 helper。
4. **粗糙度导数模型先过 profile contract**：`dy/dx`、`d²y/dx²` 类公式要求有序的一维物理轮廓。闭合外轮廓、会回折的二维边界必须先提中心线或按弧长重新参数化，不能直接当 `y(x)`。
5. **Bernoulli 不确定性与热点分数分开**：二元连通事件的 Shannon entropy 必须含 `p` 与 `1-p`；仅 `-p log p` 属自定义热点分数。
6. **高熵热点不等于信息增益**：信息增益必须依赖观测模型和期望后验不确定性下降；当前局部熵/方差只能用于候选生成，不能直接叫 expected information gain。
7. **模拟/手设上游输入只能作为情景证据**：若后续三维/优化使用工程常识构造的裂隙参数而非附件实际结果，输出必须标为 scenario/sensitivity analysis，不得冒充附件结果。
8. **最终推荐逐条 replay 硬约束**：文字合同、代码阈值与最终表必须一致；任何一个最终点违反最小间距、容量、预算等硬约束，先判不可行，再谈排序。

- **相似度归一化的上界必须与上游变量实际范围一致**：使用 `1-|a-b|/M` 等有界相似度前，必须验证上游变量确实落在声明范围；若论文自身输出超过 `M`，不能继续把结果当作 `[0,1]` 融合项。


## 16. v1.32 / S034 新增证据、统计与空间约束门禁

1. **混淆矩阵先问真值从哪来**：Precision/Recall/F1/IoU 复算正确不等于标签可信。必须记录真值掩膜来源、标注者/规则、歧义处理、是否与阈值/权重调参独立，以及原图/钻孔级切分。
2. **p 值必须可追溯**：只写 `p<0.01` 不算显著性证据。至少记录检验名称、统计量、样本单位、样本量、配对/独立结构和原假设；缺任一关键项则标为 provenance unresolved。
3. **伪代码输出参数必须有生成原语**：输出列表出现参数但正文步骤没有初始化、估计或更新该参数时，方法合同不完整，不能从结果表反推“代码一定实现了”。
4. **Bootstrap 要检查 estimator 与区间顺序**：重采样后应使用与主模型一致或明确说明的估计器；百分位置信区间通常按 `[q(alpha/2), q(1-alpha/2)]` 排列，反序必须纠正或说明。
5. **高分辨率收敛值不是物理真值**：不同采样方法趋于同一 dense-grid 数值，只证明数值稳定/收敛。没有独立测量真值时写 `numerical reference`，不得写 `true value/accuracy`。
6. **[0,1] 因子乘积仍可能只是兼容度分数**：条件独立假设不能自动把工程启发式函数校准成概率；需要标签/似然/校准评估才能叫 probability。
7. **覆盖度不等于后验不确定性，覆盖改善不等于 EIG**：距离衰减+IDW 等确定性场应标为 coverage/information surrogate；EIG 需要观测模型和对未来观测的期望后验更新。
8. **成对硬约束必须覆盖完整集合**：新增设施/测点的安全间距要明确 `new-new` 与 `existing-new`；若工程规则适用于全部位置，两类都要在最终推荐前逐点 replay。
9. **“代码见附件”只有拿到附件才算代码审计**：论文仅引用补充代码而实际文件不可访问时，最多保持 R1；伪代码和结果图不能替代 R2 的静态代码审计。

## 17. v1.33 / S035 新增泄漏、拟合拒绝与 Monte-Carlo 语义门禁

1. **先去重再切分**：图像/文件/对象存在内容重复或同源副本时，先做 hash/perceptual/source 去重与 group registry，再划 Train/Dev；重叠样本上的异常高性能按 leakage evidence 处理。
2. **没有真实时间轴不要升级时序模型**：单帧地质图像中的永久裂隙概念不能自动推出 LSTM/时序建模；只有同位置多时刻重复观测且部署也有序列输入时才进入候选竞争。
3. **物理固定周期优先降低自由度**：圆柱展开等已知几何给出 `P=pi*D` 时，先固定频率拟合；只有独立畸变/标定证据显示该合同失效才释放 P。
4. **fit success 不是 accept**：几何拟合统一检查 residual、inlier/coverage、missingness、参数物理范围和跨周期稳定性；高误差/高缺失返回 `reject/unmodelled`。
5. **Monte-Carlo 只负责传播已声明的不确定性**：抽样均值的量纲不因抽样而消失；角度均值仍是角度，不能直接称概率。Monte-Carlo 传播不等于概率校准。
6. **自归一化 `[0,1]` 输出保持 score 语义**：若没有标签/likelihood/calibration curve，角度、距离、JRC 等映射后的融合量称 compatibility score。
7. **插值离散度不是 posterior**：IDW/空间插值产生的方差或覆盖热图只能叫 spatial uncertainty/coverage surrogate；升级 posterior 需要观测模型与更新规则。
8. **论文只给 source path 仍不算代码审计**：能看到 `src/core/*.py` 文件名不等于拿到代码；R2 必须有打印/附件源码可静态追踪。

## 18. v1.34 / S036 与 2025-C 题组闭环门禁

1. **augmentation 之前冻结原始 source split**：外部数据与项目图像可合并训练，但项目目标图必须在任何 `ConcatDataset`、patch、增强之前预留 source/original-image holdout；训练使用全部目标图后不能再把全部目标图指标叫 test performance。
2. **多指标 winner 先定义 utility**：R²/RMSE/tail violation 等指标冲突时，预先指定 primary metric、成本函数或 Pareto/lexicographic 规则；禁止用“综合最优”掩盖某一关键指标恶化。
3. **图论结论只从 edge registry 生成**：阈值后的边表是 connected components、path、degree、cluster size 的唯一真相源；每次阈值改变都自动重算网络统计。
4. **一条无向边最多直接连接两个节点**：若正文同时声称 only-one-edge 与四节点连通分量，直接触发 graph-contract contradiction，阻断结果发布。
5. **[0,1] weighted similarity 仍不是 probability**：空间/产状/JRC 加权分数只有经过标签校准或显式生成模型才能升级为概率。
6. **Bayesian/EIG 词汇要求执行原语**：必须找到 prior/likelihood/posterior update，以及对未来观测取期望的效用；只有热点/模糊度/覆盖下降属于 heuristic value-of-information surrogate。
7. **2025-C 最终推荐不选论文冠军**：Q1 label-budget+source-split routing；Q2 topology/density fragments + `P=pi*D` + fixed-frequency robust fit/reject；Q3 ordered physical profile + canonical JRC + sampling-budget sensitivity；Q4 deterministic geometry + explicit compatibility + edge replay + hard-feasible sequential sensing。复杂增强模块需独立证据晋升。
## 11. v1.35 新增通用证据门禁

- **最终解码对象硬约束回放**：编码、变异或中间状态满足约束不够；任何 bridge/repair/decode 后必须在最终对象上重新检查硬约束。
- **校准锚点与验证目标分离**：若用某对象/专家先验强制标定为满分，不能再以“该对象排名第一”作为独立准确性证据。
- **聚类后同特征显著性降级**：使用同一特征生成聚类标签，再对同一特征做 ANOVA/p 值，只能视为描述性/post-selection 证据；独立验证需外部标签、留出特征或重采样稳定性。
- **全高相似度不是泛化证据**：高维余弦相似度若几乎全体接近 1，应检查标准化、维度集中与空模型/置换基线，不能直接解释为“模型泛化”或“文化规律已证明”。
- **异常回退必须显式**：PCA/聚类/优化失败时若使用默认向量，必须记录 failure/missingness provenance；禁止宽泛 `except` 静默产出看似正常的特征。

## 19. v1.36 / S043 新增评分尺度、最优性与相似度统计门禁

1. **有界加权分数先推导理论值域**：若所有分量已归一化且权重和为1，结果原则上不能无解释地超过该凸组合值域；等级表/结果表越界时必须找到额外缩放或判为 formula-scale drift。
2. **启发式算法不能自行证明 Gap=0**：GA/SA/PSO 等声称“全局最优/Gap=0”时必须登记 exact bound、solver certificate 或穷举下界；否则只能叫 best-found empirical solution。
3. **标量加权和不是 Pareto 搜索**：多目标问题被权重合并后是单目标 scalarization；需要 Pareto front 时保留向量目标或 epsilon/非支配机制，并登记目标归一化与单位。
4. **相关系数必须有配对样本轴**：`corr(x,y)` 先声明每一对观测的原子单位；两个园林级/任务级标量不能在单对象内凭空计算相关。
5. **基准对象必须通过 self-replay**：强制某 reference=100 后，再代入相似度和调整公式必须仍闭合为该基准；若自相似增益使其>100，应显式归一化/截断并只保留一个真相源。
6. **相似度矩阵是所有统计的唯一真相源**：mean/std、最高最低 pair、cluster 内均值、热力图文字和摘要都从同一矩阵自动生成；禁止手抄后漂移。
7. **Ward 需要欧氏合同**：若输入是任意融合相似度矩阵，不得直接默认 Ward 有效；应回到合法欧氏特征空间或改用与距离兼容的 linkage。
8. **相似性通常不具传递性**：`A~B, B~C` 不自动推出 `A~C`，聚类也不依赖该假设。
9. **外部误差/准确率必须有外部真值**：三两个验证对象上的“预测误差/聚类准确率”只有在 reference similarity/class label 独立定义时才是 accuracy evidence。
10. **论文声称附件有代码但当前拿不到源码时停留 R1**：公式、伪代码和可视化审计不能替代 R2 静态代码审计。
11. **自适应公式必须做单调性回放**：声称“越收敛/越低多样性越提高变异率”时，对低/中/高状态点直接代入；若公式导数方向与文字相反，按 formula-prose drift 处理。
12. **种群内 Min-Max 会让 utility 跨代漂移**：当前 generation 的 `min/max` 只能用于当代相对选择；跨代收敛、早停和结果比较默认保存 raw objective，并优先固定 reference range 或保留 Pareto 向量。
13. **AHP 判断矩阵必须来自独立比较判断**：若直接写 `a_ij=w_i/w_j` 再由特征向量求 `w`，只是已知权重的恒等回放，不是权重来源。
14. **`p>0.05` 不能证明共性/等价**：小样本不显著可能只是低功效；共性需要效应量与置信区间、等价界或跨样本稳定性。
15. **外部分类/相似度误差先冻结 truth contract**：类别标签、pairwise similarity truth 或专家偏好必须在模型预测前独立定义；模型自己的聚类/相似度不能同时充当 ground truth。
16. **聚类类型跨表使用 taxonomy_id/run_id**：后续雷达图、排名、类型均值若使用新标签，必须显式声明新 taxonomy；禁止无说明换组。



## 20. v1.37 / S044 新增代码真实性、成对样本与验证指标门禁

1. **算法名必须落到可达的定义性原语**：论文写 IGA/NSGA/深度度量/NeRF/HMM，不代表附录代码已经实现。至少找到 population/selection/crossover/mutation、训练 loop、PH/HMM/NeRF 等定义性步骤；否则只能按实际较简单 primitive 学习。
2. **真实数据结果链禁止随机占位**：缺失的分形维数、NNI、开放度等不能用 `random`/`np.random` 填入后继续生成真实园林排名。模拟数据必须独立标注 synthetic，且不得混入正式 Result Registry。
3. **固定答案不能覆盖计算输出**：模型计算之后再用字典写死排名/分数，只能作为测试 fixture，不能作为论文结果生成链。
4. **验证指标禁止 clamp/floor/常量化**：R²、MSE、MAE、CV 结果必须从 registered `y_true/y_pred/split` 纯计算产生；为了“看起来合理”把 R² 裁到 `[0.75,0.95]` 或直接返回固定 CV 数值，均按 invalid evidence。
5. **成对/三元样本的独立单位仍是实体**：10个园林可产生很多 pair，但不会产生更多独立园林。若目标是泛化到新园林，必须先按 garden/entity 分组划分，再在各折内部构造 pair/triplet。
6. **多模态/多机制分量必须有独立来源和原语**：若 topology/behavior/visual/text 都由同一个 embedding 距离代替，应改名为 shared proxy，不能继续声称已实现持久同调、HMM 或真正多模态融合。
7. **自相似矩阵对角线不是验证证据**：`S(i,i)=1` 属于构造恒等性质；亮对角线只能检查实现一致性，不能证明泛化、聚类正确或美学真实性。

## 21. v1.38 / S045 与 2025-F 题组闭环门禁

1. **路线遗传算子必须保持图可行或最终修复回放**：节点序列单点交叉/随机替换不能凭文字宣称“保持连通”；每个 child/bridge/repair 后重新检查每一跳是否为合法边、是否穿越障碍、长度/重复/入口出口等硬约束。
2. **目标函数组成必须跨公式闭合**：正文说包含长度/趣味/重复而公式漏掉长度，或前一节 Cost 与后一节 fitness 使用不同分量时，按 objective-semantic drift 处理；统一 raw objective registry 后再 scalarize。
3. **空间概率模型名称必须落到实现原语**：GMM-MRF 至少要有 Gaussian likelihood、邻接/Potts energy、EM/ICM/MAP 或等价求解以及 K-selection 证据；坐标 KMeans 不能作为 GMM-MRF 已实现的代码证据。
4. **灵敏度排序必须同一实体轴**：每个参数扰动 run 必须输出完整 `entity_id -> score`；Kendall/Spearman 比较的是不同 run 的实体排名。参数场景向量与实体分数向量即使长度相同也不可比较。
5. **`mu±1.96*sigma` 先声明 estimand**：扰动样本 SD 给出的更接近分布/参考区间；均值置信区间需要 SE/bootstrap 等。CI、prediction/reference interval 分开命名。
6. **异数量纲 cosine 先做特征尺度合同**：cosine 只对整向量的共同缩放不变，不对特征单位变化不变。长度/计数与 `[0,1]` 比例混合时，先在 train/reference cohort 拟合标准化/鲁棒缩放或块权重。
7. **Jaccard 类型必须实名**：阈值集合的 `|A∩B|/|A∪B|` 是 set Jaccard；连续比例的 `sum(min)/sum(max)` 是 weighted/min-max Jaccard（Ruzicka 类）。跨章节切换不能保持同一未注明语义。
8. **外部新对象不等于外部准确率**：把模型跑到新园林/新区域只能证明 applicability。要宣称 accuracy/generalization，需要预测前冻结的外部 target、专家偏好、类别或下游任务 truth。
9. **禁止局部事后改相似度**：负值、异常值必须通过一个预先登记、全局一致、无目标泄漏的 transformation 处理，并同时保存 raw/transformed；只改选定 pair 直接判 Result Registry provenance invalid。
10. **视觉公式核验优先于损失型文本抽取**：绝对值、上下标、根号、分式等在 `pdftotext` 丢失时，以原 PDF 渲染页为准并记录 `page/equation/resolution`。
11. **2025-F 最终推荐不选论文冠军**：Q1 采用可行几何图+透明视景变化+exact/k-shortest/RCSP/epsilon；Q2 采用确定性可解释指标+简单聚类 baseline+非循环校准+实体轴敏感性；Q3 采用紧凑标准化特征+类型匹配 similarity+单一矩阵 registry+外部 truth gate。复杂 GA/GMM-MRF/深度多模态方法只有在真实原语、独立样本和同预算增益下晋级。
12. **Train 完成后切换到能力验证而非打开 Test**：32篇 Train 全部 reviewed 后，优先冻结 Core 做 Mini Transfer / clean Dev；Test 仍保持答案、代码、图表、参数和结论不可见。



## 22. v1.39：Dev 数据合同审计增量（历史封存状态）（历史封存状态）

S013 完成的是冻结独立解答后的 Dev 调优，不能进入 Train 检索，也不证明 Core 能力增益。32篇Train保持完成，2024-D题组仅S013完成，S014–S016未读，Test仍冻结。
涉及多源表连接、年度/窗口聚合、指数标签、空间摘要或跨图表结果比较时，读取 [数据合同审计增量](references/dev-data-contracts-v139.md)。它扩展既有实体、schema、类别和Result Registry门禁，不另建角色Skill。可执行局部合同见 scripts/data_contracts_v139.py；测试通过只支持对应合同。


## 23. v1.40：当前发布状态与数值合同增量

当前稳定版本与访问状态以根目录RELEASE_MANIFEST_V140.json为准；此前各版本章节描述当时状态。S013/S014为已评审Dev，S015/S016仍待评审，32篇Train完成。2024-F/2025-D已在独立答案冻结后完成历史评价，不能重新当freshblind；这次没有将Test知识推广到Core。禁止因封版自动打开新论文。

遇到多级平均、地理栅格、循环变量、层级权重或跨总体指标比较时，读取[数值与评价合同增量](references/dev-numerical-contracts-v140.md)。这是既有实体/单位/Result Registry/组合门禁的扩展，不是另一套角色Skill。审计局部函数和反例位于learning_output/analyses/dev_2024D/S014/audit_replay.py；它们不等于生产就绪的完整地理模型。

新题试用以题面/官方数据为输入，先数据审计、每问模型竞争、可执行Baseline和独立验证；复杂模型仅在可比独立验证中有稳定实质提升才晋级。学习审计PASS与真实新题表现分开；正式比赛交付继续复用本包现有S0–S8流程，不另造角色Skill。


## 24. v1.41 / 2024-D Dev 题组闭环

2024-D 的独立解答先于 S013-S016 访问完成并冻结。四篇 Dev 论文对照只用于发现通用缺口，不把题目特定答案、阈值、未来风险数值或作者排行榜写回普通 Train retrieval。

遇到统计对象漂移、重采样基率、伪标签/目标派生特征、未来地图、组成边际/转移流量、output space、极端尾部或跨程序文件接口问题时，读取 `references/dev-casegroup-contracts-v141.md`。

高频门禁：
1. `sum/mean/SD/variance/rate/fraction` 必须登记 support/operator/unit/denominator/source。
2. 重采样只在训练折；抽样后的类别比例不得直接当部署总体风险。
3. 保存 `label_source / forecast_origin / available_at / prediction_scope`；目标后代不能进入部署预测器。
4. `fitted/OOB/CV/holdout/rolling/spatial-block` 分开登记；未来地图不是回测。
5. 两期组成边际不能唯一识别真实类间转移；没有实体轨迹或额外识别假设不得声称流量。
6. probability/logit/raw margin/SHAP/class score 明确 output space 与 class/link。
7. 跨 CSV/程序/栅格接口核唯一键、header、shape、CRS/transform 和实际读取文件 hash；源文件 hash 不能替代求解器真实输入。

2024-D Mini Transfer Test 为 post-Dev synthetic mechanism transfer，状态 `PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX`。它不是 clean blind、不是 R7，也不建立 v1.41 对 v1.40/No-Core 的因果能力增益；Controlled Core Ablation 仍为 `NOT_RUN`。
