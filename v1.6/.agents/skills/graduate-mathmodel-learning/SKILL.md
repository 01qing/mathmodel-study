---
name: graduate-mathmodel-learning
description: 面向全国研究生数学建模竞赛的长期学习与复盘 Skill。基于现有 MathModel-Skill Standard/Codex 工作流，提供深度题解、候选模型竞争、优秀论文批判性精读、数学到代码映射、风险与失效条件、独立训练、知识卡沉淀和跨会话学习状态。正式比赛模式必须交回 paper-workflow-orchestrator，禁止绕过原 S0-S8 证据链。
---

# Graduate MathModel Learning

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

统一状态：
`author_claim | verified | partially_verified | not_verified | contradicted | our_inference`

代码未实际运行，不得将其数值结果或完整复现标记为 `verified`。静态数据流或公式核验可以记录具体发现，但必须标明核验范围，不能推广为整体代码正确。
论文自报奖项未从可信来源核验时，不得写成已核验奖项。

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
