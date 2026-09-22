# Graduate MathModel Learning Skill v1.6

当前版本说明见 `PROGRESS_V16.md`，验证结果见 `VALIDATION_V16.json`，继承关系见 `UPSTREAM_LOCK.json`。以下v0.4至v1.5文字保留为历史记录，不代表当前资料获取状态。

这是建立在 `yushui2022/MathModel-Skill` 之上的完整 Codex Skill 扩展初版。

## 已包含

- 真正的 `.agents/skills/graduate-mathmodel-learning/SKILL.md`
- 6 个 reference
- 6 个脚本
- 6 个模板
- 5 类模式 eval
- 安装说明
- smoke test 报告

## 当前定位

这是“可运行的工程骨架”，还没有大规模灌入 2021-2025 研赛资料。

下一步应该选一套真实研赛题跑通：
原题 + 2篇优秀论文 + 附件 + 代码（若有）。

真实使用反馈再决定 v0.5 修改，而不是继续空想功能。


## v0.5 新增

- 2021–2025 研赛资料元数据目录
- 来源等级与冲突治理
- `case_manifest`
- 第一套验收案例 `gmcm-2021-D`
- source catalog 校验
- case workspace 自动创建
- source-conflict eval

注意：v0.5 仍不把大体积 PDF/XLSX 塞进 Skill。资料在实际项目中落到 `learning_sources/`。


## v0.6 新增

- 2021 D 题名冲突完成内容级消歧
- 选定两篇方法差异明显的首组主论文
- `paper-screening-2021-D.md`
- `blind-baseline-2021-D.md`
- E7 真实题 blind model-selection eval
- 防止“看过优秀论文后伪装独立解题”的隔离规则
- Q3 采样/CV 数据泄漏检查
- Q4 描述符可行域与真实分子可实现性检查


## v0.7 新增

- problem-statement-only facts contract
- ADMET favorable direction contract
- CYP3A4 ambiguity guard
- contaminated reference baseline
- 100-point fresh blind eval rubric
- blind bundle preparation / contamination validation scripts
- Q4 feasibility/manifold guard


## v0.8

新增真实 Excel 数据审计门禁；当前真实 2021 D XLSX 统计保持 NOT_RUN，禁止用题面数字冒充实测结果。


## v0.9

新增可执行 Leakage-Safe Benchmark：

- Q1 selector + Q2 regressor 作为同一 nested-CV Pipeline
- Q3 五个 ADMET 标签独立选模
- balanced accuracy / MCC / PR-AUC 等多指标
- 特征选择稳定性
- practical tie
- 推荐理由、第二名和切换条件
- 官方 test 集完全隔离

真实 2021 D benchmark 仍为 `NOT_RUN`，当前只完成 synthetic smoke。


# v1.0

第一版完整工程闭环：

`资料治理 → 数据审计 → 无泄漏选模 → Final Fit → Test 预测 → 优秀论文对照 → 知识沉淀`

注意：v1.0 的“完成”是 Skill 工程第一版完成。真实 2021 D 数据、Fresh Blind Eval 和论文数值复现仍保持 NOT_RUN，不能把 synthetic smoke 当成真实赛题结果。


# v1.1

新增真实公开参赛代码审计能力。

首个真实代码对象：`Bureaux-Tao/modeling2021-D`。

新增：
- 训练/验证/test 数据流审计
- scaler/PCA fit-transform 边界检查
- metric API 参数顺序检查
- holdout 重复使用检查
- 通用 ML 静态风险扫描器
- 真实 2021 D 外部代码审计资产

注意：代码文本问题已经核验，但公开 CSV 尚未在当前运行容器完整落盘，因此数值复现和真实 benchmark 仍为 `NOT_RUN`。


# v1.2

新增真实数据来源获取与交叉核验层：Git blob SHA/size 验证、XLSX contest-attachment mirror、participant CSV mirror、CSV 审计和 XLSX-vs-CSV 语义等价性门禁。

当前环境仍不能完整物化 8.8MB XLSX / 6.4MB CSV，因此真实数据 benchmark 保持 NOT_RUN。


# v1.3

加入第二真实迁移案例 `gmcm-2024-C`。

目标不是再做一套机器学习题，而是验证 Skill 是否能从 2021 D 的表格建模迁移到：

`波形分类 → Steinmetz机理修正 → 因素交互 → 跨工况预测 → 双目标优化`

新增：
- 2024 C problem facts / case manifest
- 2024 C learning route
- 2021 D → 2024 C cross-case transfer
- generic learning-case builder
- E17–E21 migration evals


# v1.4

第二迁移案例开始接受真实代码证据。

新增：
- 2024 C Q1/Q2/Q4/Q5 public-code audit
- Q3 unresolved evidence guard
- Q5 objective-completeness check
- excellent-paper vs solution-profile boundary
- E22-E27

关键发现：公开 Q5 PSO 的已核验目标函数只最小化磁芯损耗，未编码题目要求的 `maximize f*Bm` 第二目标。


# v1.5

核心不是增加算法，而是修正学习实验顺序。

2024 C 因为先看过公开代码/获奖方案，正式降级为：
`RETROSPECTIVE_INDEPENDENT_ROUTE_NOT_FRESH_BLIND`

新增：
- 2024 C 独立 Q1-Q5 模型竞争矩阵
- solution-exposure / blind-contamination 记录
- `start_blind_case.py`
- `freeze_blind_matrix.py`
- 2024 优秀论文百度云入口/提取码的持久化访问队列
- E28-E33

这保证下一道真正未接触的题可以第一次严格完成：
`题面 -> 独立模型竞争 -> 冻结 -> 论文/代码 -> 对照学习`


# v1.6（当前）
本包从用户v1.5完整复制后增量修改，同时包含固定提交的上游十个Codex Skill；原始进度文档是历史记录。当前变更与验证见PROGRESS_V16.md和VALIDATION_V16.json。没有运行完整S0–S8，不能据安装依赖齐全宣称正式论文生产链通过。
