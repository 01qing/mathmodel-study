# MathModel-Skill v2.3.0 原版架构审查与研赛学习扩展边界

## 1. 审查结论

本文件基于 `yushui2022/MathModel-Skill` 的 `standard` 分支、Codex 包和 10 个现有 Skill 进行结构审查。

核心结论：

1. 原版 MathModel-Skill 的本质是“正式比赛论文生产与证据验证流水线”，不是长期教学系统。
2. `paper-workflow-orchestrator` 是完整论文任务的唯一总入口，S0-S8 是正式流程的权威顺序。
3. 新的“全国研究生数学建模竞赛学习 Skill”不应改写 S0-S8，也不应复制原有审题、选模、清洗、代码、QA、写作能力。
4. 新 Skill 应读取原版已经生成的结构化中间产物，在其上增加：
   - 深度教学解释
   - 候选模型竞争与排除理由
   - 优秀论文批判性精读
   - 风险、失效条件、替代方案
   - 可迁移方法卡与题型卡
   - 独立做题训练
   - 长期学习状态
5. 正式比赛模式仍由原 `paper-workflow-orchestrator` 接管；学习模式不能擅自伪装成正式 S0-S8 PASS。

---

## 2. 原 Codex 版 10 个 Skill

### 2.1 paper-workflow-orchestrator
角色：正式比赛完整任务总调度器。

正式链：

S0 输入接纳  
→ S1 题意分析  
→ S2 模型与评分路线  
→ S3 数据与可视化计划  
→ S4 可复现建模代码  
→ S5 真实运行  
→ S6 证据门禁  
→ S7 正式论文写作  
→ S8 格式与渲染门禁

扩展策略：**完全复用，不修改主链。**

---

### 2.2 problem-doc-model-selector
角色：
- 解析题面与附件
- 识别每一问
- 提取目标、约束、数据条件、输出要求
- 初步判断任务类型和模型路线
- 输出 `paper_output/step1/problem_analysis.json`

扩展策略：**强复用。**

研赛学习 Skill 应优先读取其结构化题意结果，而不是重新从零做第二套题面解析器。

需要补充的不是“再选一次模型”，而是：
- 为什么把这一问抽象成这一类数学问题
- 数据字段怎样映射成变量
- 哪些抽象存在歧义
- 如果换一种抽象会导致什么模型路线

---

### 2.3 modeling-paper-rubric-and-model-selector
角色：
- 基线模型
- 1-2 条改进路线
- 验证计划
- 风险与备选
- 评分点与证据对齐
- 输出 `paper_output/plan/model_route.json`

扩展策略：**强复用，但这是最需要“教学增强”的位置。**

原版解决：
“比赛中应该用什么路线并如何拿分。”

新 Skill 解决：
“为什么这样选；为什么不用其它合理方法；什么条件下应该改选。”

因此禁止重新建立一个平行的“模型选型器”。

---

### 2.4 authoritative-data-harvester
角色：
- 找权威公开数据
- 优先官方 API / bulk download
- 记录来源、口径、访问日期
- 写入 `crawled_data/`

扩展策略：**按需复用。**

学习优秀论文时也可用于核验论文使用的外部数据来源，但它不是论文检索器。

---

### 2.5 data-cleaning-and-visualization
角色：
- 数据读取诊断
- 数据清洗
- 数据计划
- 可视化计划
- 论文级图表
- 输出 cleaned data / figure index

扩展策略：**复用执行能力，增加解释层。**

新 Skill 不重复写清洗脚本，而应该解释：
- 为什么该缺失处理合理
- 为什么不采用另一种插补
- 异常值处理会不会改变结论
- 哪种图真正回答题目，哪种只是装饰

---

### 2.6 model-code-and-result-generator
角色：
- 根据模型路线生成当前赛题专用 q*_model.py 脚手架
- 执行真实模型
- 生成 machine-readable 结果、指标、结论和运行 manifest
- 禁止把占位结果冒充正式结果

扩展策略：**强复用。**

新 Skill 应在学习模式增加：
“数学式 → 算法步骤 → 代码模块 → 输出结果”的逐层映射，
而不是再造一个代码生成器。

---

### 2.7 quality-assurance-auditor
角色：
- 正式证据 Gate
- 检查题目覆盖、模型任务匹配、逻辑闭环、证据新鲜度、图表链等
- FAIL 时阻塞后续正式流程

扩展策略：**复用正式验证结果，但新增教学型 QA。**

原 QA 重点是：
“这份比赛产物能不能继续进入正式论文。”

学习型 QA 还要问：
- 为什么错
- 错误属于概念、数据、模型、实现还是验证
- 这种错误以后如何识别
- 应沉淀成哪条个人错误模式

两种 QA 不应混为一谈。

---

### 2.8 paper-formal-writer
角色：
- S7/S8 唯一正式论文写作者
- 章节写作
- 全文统一
- DOCX
- 公式 OMML
- 版式与渲染检查

扩展策略：**比赛模式复用；学习模式默认不调用。**

学习题解、论文精读和训练反馈不应该被强制写成 14000 字正式竞赛论文。

---

### 2.9 paper-micro-unit-generator
角色：
- 正式 S7 中反复失败段落的局部修复
- legacy/quickstart scaffold

扩展策略：**通常不参与学习模式。**

不能把它误用成“逐段教学生成器”。

---

### 2.10 context-memory-keeper
角色：
- `memoryskill.md`：长期准则 + 当前短期工作台
- `memory_archive.md`：旧任务归档
- `paper_output/context/workflow_memory.json`：正式 S0-S8 可执行断点状态
- guard 报告优先于聊天记忆

扩展策略：**复用其“项目/工作流记忆”思想，但学习记忆单独建。**

原因：
- workflow memory 表达“这道正式赛题做到哪一步”
- 学习 memory 表达“用户掌握到什么程度、学过什么、弱点是什么”

两者生命周期和数据结构不同。

建议：
- 不修改 `workflow_memory.json`
- 不把几百篇论文学习记录塞进 `memoryskill.md`
- 新增独立 `learning_output/context/learning_state.json`
- 可在 `memoryskill.md` 只保留一个轻量链接/摘要

---

## 3. 原版正式调用关系

```text
paper-workflow-orchestrator
│
├─ S0 preflight / manifest
│
├─ S1 problem-doc-model-selector
│
├─ S2 modeling-paper-rubric-and-model-selector
│   └─ 若需要外部公开数据
│       └─ authoritative-data-harvester
│
├─ S3 data-cleaning-and-visualization
│
├─ S4 model-code-and-result-generator
│
├─ S5 run_modeling.py 真实执行
│
├─ S6 quality-assurance-auditor
│
├─ S7 paper-formal-writer
│   └─ 仅当反复失败且 repair_queue 指定
│       └─ paper-micro-unit-generator
│
└─ S8 paper-formal-writer format/render gate

所有重要阶段
└─ context-memory-keeper
```

---

## 4. 一个需要注意的原版内部表述不一致

`problem-doc-model-selector` 某些说明段落中提到“后续通常先做 data-cleaning-and-visualization”，
但它的执行契约同时明确写了：
`problem_analysis.json` 应交给 `modeling-paper-rubric-and-model-selector`。

总编排器 S0-S8 也明确规定：
S1 problem analysis → S2 model/rubric → S3 data/visualization。

因此扩展 Skill 必须遵循：

**orchestrator + workflow_guard > 子 Skill 中的非契约性提示文字。**

不能因为某一段旧说明而跳过 S2。

---

## 5. 我们的新 Skill 绝对不能重复的能力

以下内容直接复用原版：

- PDF / Word 赛题解析基础能力
- 问题编号与附件识别
- 基础任务类型识别
- 正式模型路线 JSON
- 正式评分点对齐
- 官方数据获取
- 数据清洗执行
- 图表生成执行
- 建模代码执行
- 真实结果 manifest
- 正式 evidence gate
- 正式论文生成
- DOCX / 渲染 QA
- 正式 S0-S8 工作流状态

否则会形成两套真相源。

---

## 6. 新 Skill 必须新增的能力

### A. 深度题解层
对每一问增加：
- 自然语言 → 数学结构
- 变量 / 参数 / 目标 / 约束映射
- 数据字段 → 模型变量
- 关键假设
- 公式来源与推导
- 求解逻辑
- 结果的数学含义

### B. 候选模型竞争层
至少：
- 最小可用基线
- 推荐主方案
- 一个真正合理的替代方案

比较：
- 结构匹配
- 假设
- 数据需求
- 可解释性
- 精度潜力
- 样本风险
- 调参成本
- 实现难度
- 竞赛时间风险
- 验证难度
- 创新空间

必须给明确倾向，不允许只写“各有优缺点”。

### C. 优秀论文精读层
区分：
- 作者事实
- 作者主张
- 已核验
- 部分核验
- 未核验
- 我们的推断
- 我们的改进

支持多篇论文逐问比较。

### D. 教学型验证
除正式 QA 外，记录：
- 为什么错
- 怎样发现
- 错误属于哪一类
- 下次的识别规则

### E. 知识沉淀
形成：
- 方法卡
- 题型卡
- 论文复盘卡
- 比赛经验卡
- 个人错误模式

### F. 长期学习状态
记录掌握等级：
- unseen
- introduced
- can_explain
- can_apply_with_help
- can_apply_independently
- can_compare_and_adapt

### G. 独立训练模式
先让学习者独立判断，再对照：
- 学习者路线
- 优秀论文路线
- 原版 Skill 正式路线
- 我们的综合判断

---

## 7. 新 Skill 与原版的正确集成方式

新 Skill 不作为 S0-S8 的第 S9。

更合理的是“旁路教学层”：

```text
                      ┌─ 研赛学习 Skill ─────────────────────┐
                      │  解释 / 比较 / 精读 / 训练 / 沉淀    │
                      │                                      │
S1 problem_analysis ──┼──────────────→ 深度审题              │
S2 model_route ───────┼──────────────→ 模型竞争              │
S3 data_plan ─────────┼──────────────→ 数据处理理由          │
S4/S5 results ────────┼──────────────→ 数学-代码-结果映射    │
S6 evidence ──────────┼──────────────→ 可信度与失败原因      │
优秀论文/解析 ─────────┼──────────────→ 论文批判性精读        │
                      │                                      │
                      └→ knowledge_base + learning_state ────┘
```

正式比赛：
`paper-workflow-orchestrator` 仍是最高权威。

学习：
`graduate-mathmodel-learning` 是入口，根据需要读取或调用原有子 Skill。

---

## 8. 下一阶段工程设计原则

下一步不是立即写超长 `SKILL.md`。

先设计完整目录与契约，至少包括：

```text
.agents/skills/graduate-mathmodel-learning/
├── SKILL.md
├── references/
├── scripts/
├── templates/
└── evals/
```

并定义：

1. 五种模式如何路由：
   - learn
   - competition
   - paper-review
   - review
   - practice

2. 各模式读取哪些原版 contract。

3. 新 Skill 自己只允许写哪些目录。

4. learning_state 的 JSON schema。

5. 方法卡、题型卡、论文评审卡的数据 schema。

6. 如何避免污染 `paper_output/` 正式证据。

7. 如何在切换新对话时恢复学习进度。

8. 如何判断“优秀论文中的结论已核验”。

9. 如何把真实赛题作为 eval，而不是只做静态 prompt 测试。

---

## 9. 当前冻结的架构原则

- 不 fork/复制原 10 个 Skill 的核心职责。
- 不改 S0-S8 正式顺序。
- 不把学习模式伪装为正式 evidence PASS。
- 不把优秀论文作者主张默认当成事实。
- 不把学习记忆塞进正式 workflow memory。
- 不让“更高级的算法”自动等价于“更好的竞赛模型”。
- 不以算法关键词替代问题结构识别。
- 新 Skill 的价值集中在：解释、比较、判断、复盘、迁移和长期学习。

