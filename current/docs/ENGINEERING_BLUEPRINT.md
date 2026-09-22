# 全国研究生数学建模竞赛学习 Skill 工程蓝图 v0.3

## 1. 定位

本扩展建立在 `yushui2022/MathModel-Skill` Standard/Codex 正式工作流之上。

原版负责：
- 正式赛题输入接纳
- 题意结构化
- 比赛型模型路线
- 数据清洗与图表
- 可复现建模代码
- 真实运行证据
- 正式 QA
- 正式论文与 Word 交付
- S0-S8 工作流恢复

本扩展负责：
- 深度题解
- 候选模型竞争与排除理由
- 优秀论文批判性精读
- 数学→算法→代码→结果映射
- 风险、失效条件、替代方案
- 方法卡、题型卡、论文复盘卡
- 独立做题训练
- 长期个人学习状态

## 2. 最高架构原则

1. 不复制原 10 个 Skill 的核心职责。
2. 不修改 S0-S8 正式顺序。
3. 不把学习产物写入正式 evidence contract。
4. 不把优秀论文的作者主张默认当成事实。
5. 不把学习记忆塞进 `workflow_memory.json`。
6. 原版正式 contract 是“比赛事实源”；学习 contract 是“教学事实源”。
7. `paper-workflow-orchestrator` 在 competition 模式中拥有最高路由权。
8. 学习模式可以读取原正式 contract，但无权伪造其 PASS 状态。
9. 所有跨会话学习状态必须落盘，不依赖聊天历史。
10. 任何可复现结论都应记录来源、验证状态和时间。

## 3. 推荐项目结构

```text
MathModel-Skill/
├── .agents/
│   └── skills/
│       ├── ...原有10个Skill
│       └── graduate-mathmodel-learning/
│           ├── SKILL.md
│           ├── references/
│           ├── scripts/
│           ├── templates/
│           └── evals/
│
├── problem_files/                 # 原版正式赛题输入
├── crawled_data/                  # 原版外部数据
├── paper_output/                  # 原版正式 S0-S8 产物
│
├── learning_sources/              # 学习原始资料，绝不作为正式结果证据
│   ├── source_index.json
│   └── competitions/
│       ├── 2021/
│       ├── 2022/
│       ├── 2023/
│       ├── 2024/
│       └── 2025/
│           └── A/
│               ├── problem/
│               ├── papers/
│               ├── data/
│               ├── code/
│               ├── expert_commentary/
│               └── literature/
│
├── learning_output/               # 学习过程与跨会话状态
│   ├── context/
│   │   ├── learning_state.json
│   │   └── next_learning.md
│   ├── sessions/
│   ├── analyses/
│   ├── comparisons/
│   └── practice/
│
└── knowledge_base/                # 已提炼的长期知识
    ├── methods/
    ├── problem_patterns/
    ├── paper_reviews/
    ├── competition_lessons/
    └── error_patterns/
```

## 4. 三类目录必须严格区分

### 4.1 `paper_output/`
正式比赛证据链。
只有原 S0-S8 可以决定其正式状态。

### 4.2 `learning_output/`
学习过程、解释、比较、训练反馈。
可以引用 `paper_output/`，但不反向伪造正式证据。

### 4.3 `knowledge_base/`
已经经过整理、适合长期复用的知识。
不能直接把原论文全文复制进来；应存提炼后的卡片与来源索引。

## 5. 学习扩展读取的原版 contract

优先级：

1. `paper_output/input_manifest.json`
2. `paper_output/step1/problem_analysis.json`
3. `paper_output/plan/model_route.json`
4. `paper_output/plan/data_plan.json`
5. `paper_output/plan/visualization_plan.json`
6. `paper_output/results/run_manifest.json`
7. `paper_output/results/model_results.json`
8. `paper_output/results/metrics.json`
9. `paper_output/results/conclusions.json`
10. `paper_output/qa/evidence_gate_report.json`

读取原则：
- 有结构化 contract 就不重复从自然语言猜。
- contract 之间冲突时，以 `paper-workflow-orchestrator` / `workflow_guard` 当前状态为准。
- 学习解释可以提出“原路线值得质疑”，但不能直接修改正式 PASS 状态。

## 6. 学习扩展自己的核心 contract

- `learning_output/context/learning_state.json`
- `learning_sources/source_index.json`
- `learning_output/sessions/<session_id>.json`
- `knowledge_base/methods/<method_id>.json`
- `knowledge_base/problem_patterns/<pattern_id>.json`
- `knowledge_base/paper_reviews/<paper_id>.json`

这些 contract 的 JSON Schema 位于本蓝图 `schemas/`。
