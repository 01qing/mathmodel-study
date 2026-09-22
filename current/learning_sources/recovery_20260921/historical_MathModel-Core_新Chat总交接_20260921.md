# MathModel-Core 新 Chat 总交接 — 2026-09-21

> 用途：当前长对话切换到新 Chat 时，恢复 MathModel-Core 的准确状态、冻结边界、Role Pilot 进展、2022-C paired benchmark 协议，以及下一步执行顺序。
>
> **重要：本文件用于“项目总控 / orchestration Chat”，不要把它作为 Run A 或 Run B 的输入。** Run A/B 必须保持隔离。

---

## 0. 为什么现在应该换 Chat

当前对话已经非常长，且同时包含：

- MathModel-Core 长期训练历史；
- 2023-C post-freeze 优秀论文对照；
- Architect / Reviewer role interface pilot；
- 2022-D exact model smoke fixture；
- 2022-C paired A/B benchmark 的注册、隔离协议与运行包。

继续在一个 Chat 中堆叠，会增加三类风险：

1. 历史实验日志与最终冻结结论混淆；
2. 临时 heuristic / timeout 被误记成正式证明；
3. 2022-C Run A / Run B 的上下文相互污染。

因此当前时点适合正式切换。

---

# 1. 项目总身份

当前唯一共享知识 Core：**MathModel-Core**。

现阶段原则：

- 一个共享 Core；
- Architect / Reviewer 是角色接口，不复制知识库；
- 不创建独立 Architect-Core / Reviewer-Core；
- 只有在角色效果被控制实验验证后，再决定是否推广角色化生产流程。

当前 Core：

```text
MathModel-Core v1.41.0
status = SEALED
read-only during role experiments
```

Core release identity：

```text
outer wrapper:
release-v141.zip
SHA256 = a4ef5b69d31ab2b5de032e9fa9e8c78f15a09b773bfca3ace57870cdb418016f

internal Core:
Graduate-MathModel-Learning-Skill-v1.41.zip
SHA256 = 191c4dad37c811049516c66862bd2d45d1364784ff277ec73e5667d07cb64d6f
bytes = 206263605
zip_entries = 2341
zip_test = PASS
status = SEALED
```

能力证据边界仍然是：

```text
clean_blind_core_gain = NOT_ESTABLISHED
controlled_no_core_previous_new = NOT_RUN
```

因此不能声称 v1.41 已被因果证明优于 v1.40 或 No-Core。

---

# 2. MathModel-Core 长期训练框架

长期目标不是“摘要优秀论文”，而是训练 Core 在陌生建模题上独立完成：

```text
问题识别
→ 模型竞争
→ 6小时稳妥 Baseline
→ 数学模型
→ 代码实现
→ 验证
→ 审计
→ 错误修复
→ 可迁移规则
```

主要训练纪律：

- Candidate Model Competition：Baseline / 作者方案 / 主要替代 / 不推荐方案；
- 复杂模型不能因为标签高级自动进入主线；
- first-fail 必须保留；
- 结果必须有 provenance；
- 算法名称必须还原为实际公式、数据流和代码 primitive；
- Train / Dev / Test 严格分离；
- Reproduction Level R0–R7 不得无证据升级。

45篇库身份曾验证为：

```text
45 papers
6752 chunks
32 Train
7 Dev
6 Test
```

---

# 3. 2023-C 状态：完全封存

2023-C independent solution 在优秀论文暴露前已冻结。

2023-C excellent-paper post-freeze review：

```text
10 / 10 COMPLETE
```

最终证据状态：

```text
POSTFREEZE_2023C_EVIDENCE_BUNDLE_SEALED
```

最终 ZIP：

```text
/mnt/data/MathModel-Core_v1.41_2023C_postfreeze_FINAL_EVIDENCE_SEALED_20260920.zip
SHA256 = e57e493cc622b4ca5843516e4033354153fa4228b80867cfcfb227d2b758d9d4
```

验证：

```text
27/27 recovery validation PASS
34/34 final evidence-scope validation PASS
79/79 reverse ZIP validation PASS
persistence gap = empty
```

### 绝对禁止

- 不重新解2023-C；
- 不重读10篇论文；
- 不修改冻结的2023-C independent solution；
- 不打开 2023 A/B/D/E/F 优秀论文或答案。

---

# 4. Role Pilot 的原始目的

Role Pilot 不是为了复制 Skill，而是测试：

> 在相同 MathModel-Core 下，Architect → Reviewer 的接口化工作流是否能比 single-Core generalist 更可靠地发现错误、选择模型、建立证据和修复方案。

最初使用 2022-D 作为 **pipeline smoke fixture**，不是 causal benchmark。

---

# 5. 2022-D Role Pipeline Smoke：已经完全封存

题目：2022-D PISA 架构芯片资源排布问题。

暴露边界：

- 只使用官方题面与官方 attachment；
- 未打开2022-D优秀论文、参考答案、solution code。

## 5.1 Reviewer A first-fail

Architect A 最初把一个复用同一 dependency builder 的 checker 称为“independent verifier”。

Reviewer A 判定：

```text
common-mode validation / provenance overclaim
MAJOR
Decision = HOLD
```

修复原则：

- 原 checker 改称 `internal consistency verifier`；
- 新建 raw-semantics checker，独立从原始 CSV 重建 CFG、控制依赖、数据依赖和资源约束。

first-fail 被保留，没有被删掉或改写。

## 5.2 Q1 最终闭合

Q1 完整问题：

```text
GLOBAL OPTIMUM = 54 stages
```

证明结构：

### Lower bound

H=53 THA2 projected necessary relaxation：

- 248 selected blocks；
- 使用完整607-block问题推导出的 cumulative precedence lag；
- projected weighted reduction mismatch = 0；
- HiGHS 完整搜索；
- status = Infeasible。

因此：

```text
Q1* >= 54
```

### Upper bound

找到完整 607-block H=54 schedule，并独立验证：

- precedence violations = 0；
- stage resource violations = 0；
- fold violations = 0；
- even-TCAM = 5；
- max TCAM/stage = 1；
- max HASH/stage = 2；
- max ALU/stage = 56；
- max QUALIFY/stage = 30。

因此：

```text
Q1* <= 54
```

最终：

```text
Q1 GLOBAL OPTIMUM = 54
```

Q1 evidence Library：

```text
/MathModel-Core/2022D_rolepilot_q1_optimality_20260921/
```

## 5.3 Q2 最终闭合

Q2 保留两个 folded-HASH 语义，不能混用：

### C1

```text
max-path HASH(stage k)
+
max-path HASH(stage k+16)
<= 3
```

### C2

```text
同一 CFG path 上
HASH(stage k)+HASH(stage k+16)
的联合最大值 <= 3
```

最终结果：

```text
Q2-C1 GLOBAL OPTIMUM = 40
Q2-C2 GLOBAL OPTIMUM = 40
```

### shared lower bound

14个 TCAM block 的 exact necessary subproblem：

```text
H=39: INFEASIBLE
exhaustive DFS nodes = 3121

H=40: FEASIBLE
DFS nodes = 311
```

该模型删除了非TCAM块和其它资源约束，因此是 C1/C2 完整问题的松弛；H39松弛都不可行，所以两个语义都满足：

```text
Q2* >= 40
```

### H40 full schedule 独立 replay

raw-semantics replay：

```text
607/607 blocks
max stage = 39
control pairs = 120423
direct precedence pairs = 120593
strict pairs = 3055
precedence violations = 0
max TCAM = 1
max QUALIFY = 45
max path HASH = 2
max path ALU = 47
max folded HASH C1 = 3
max folded HASH C2 = 3
even TCAM stages = {4,6,8,12,14}
```

因此同一个 H40 schedule 同时满足 C1 与 C2。

### 重要解释

C1/C2 的 optimum stage count 都是40，**不代表两个 feasible set 相同**。

## 5.4 Architect B → Reviewer B

Architect B 修复证据语义并关闭 exact registry。

Reviewer B 最终：

```text
PASS
scope = ROLE_PIPELINE_SMOKE_PASS / 2022-D Q1+Q2 EVIDENCE CLOSURE
```

但禁止升级成：

```text
ROLE_SPECIALIZATION_IMPROVES_CAPABILITY
```

因为2022-D不是严格 A/B causal experiment。

## 5.5 2022-D 最终状态

```text
FROZEN
DO NOT KEEP OPTIMIZING
```

---

# 6. 下一阶段：2022-C Paired Benchmark

Benchmark：

```text
ROLE-P1-2022C-v0.2
```

题目：

```text
2022-C 汽车制造公司涂装-总装缓存区调序调度优化问题
```

当前状态：

```text
SOURCE_FROZEN
REGISTERED
A = NOT_RUN
B = NOT_RUN
C blind evaluator = NOT_RUN
```

准备 / orchestration Chat **没有读取题面正文、没有检查工作簿单元格、没有读取优秀论文/答案/solution**。

## 6.1 官方源文件冻结身份

Run A 和 Run B 必须收到完全相同的5个官方文件：

| 文件 | bytes | Git blob SHA-1 |
|---|---:|---|
| `2022C_官方题面_汽车制造公司涂装-总装缓存区调序调度优化问题.docx` | 388087 | `d11123561801c4f15e308b55b72ff97a7f4e24b8` |
| `2022C_附件1.xlsx` | 15262 | `3ad2e09e579bf65c0435789e101fd7d2c9a0d9e5` |
| `2022C_附件2.xlsx` | 15402 | `c5747522b104cc1fb2c2814feeec2ab215a76be7` |
| `2022C_附件3.xlsx` | 10138 | `a297c0a708cdaf88769614f01b9b5dc177d01535` |
| `2022C_附件4.xlsx` | 9196 | `50d1da619d1269949833614935d5eb0cba75219d` |

### 暴露边界

在 Run A、Run B、Blind evaluator 全部冻结之前，禁止：

- 2022-C优秀论文；
- 参考答案；
- solution blog/article；
- solution GitHub/code；
- 针对2022-C模型解法的网页搜索；
- 把 A 输出传给 B；
- 把 B 输出传给 A。

---

# 7. 2022-C v0.2 运行包

v0.2 supersedes v0.1 作为正式运行包。

A/B v0.2 已内嵌真实验证过的 sealed v1.41 wrapper。

## Run A

```text
ROLE-P1-2022C_RUN_A_SINGLE_CORE_v0.2.zip
SHA256 = 3843ca8acce9b13e7da58fdaa922592cf7ef9c28f535db9b5499f9759310f538
```

内容包括：

- `release-v141.zip`
- release sidecar / release JSON
- Core identity gate
- contamination guard
- official source identity manifest
- common frozen contract
- Run A prompt
- README

## Run B

```text
ROLE-P1-2022C_RUN_B_ARCHITECT_REVIEWER_v0.2.zip
SHA256 = 90c439f1f6063cad52e5a33ec498193a6b329dc624871d32f5eca22a8653ec9f
```

额外包括：

- Architect Interface Contract
- Reviewer Interface Contract

## Run C

```text
ROLE-P1-2022C_RUN_C_BLIND_EVALUATOR_v0.2.zip
SHA256 = 2b8d4612efab7e57db87a46fada562222b8631b7d7db64ea8bda392b3d81b2f5
```

Run C 不带 Core，因为它只负责 blind evaluation。

## Orchestration pack

```text
ROLE-P1-2022C_ORCHESTRATION_TEXT_PACK_v0.2.zip
SHA256 = f3505db2aeef710929dd14f17a84d162b201d2a6e0f3533f1d73fa36afff7bd5
```

Library 持久化路径：

```text
/MathModel-Core/ROLE-P1-2022C_v0.2/
```

---

# 8. A/B/C 隔离执行协议

必须使用三个 fresh chats。

## Chat A — Single-Core Generalist

只上传：

1. `ROLE-P1-2022C_RUN_A_SINGLE_CORE_v0.2.zip`
2. `2022C_官方题面_汽车制造公司涂装-总装缓存区调序调度优化问题.docx`
3. `2022C_附件1.xlsx`
4. `2022C_附件2.xlsx`
5. `2022C_附件3.xlsx`
6. `2022C_附件4.xlsx`

**不要上传：**

- 本总交接文件；
- Run B；
- Run C；
- 2022-D总结；
- A/B比较目标之外的提示；
- 优秀论文/答案。

Run A 预算：

```text
GPT-5.6 Sol / High
max 40 tool calls
target 60 min
Pass 1 independent solve
Pass 2 self-audit
Pass 3 at most one repair
```

Run A 完成后必须冻结：

1. initial artifact；
2. self-audit；
3. final artifact；
4. Result Registry；
5. execution/failure log；
6. claim limits。

## Chat B — Architect → Reviewer

必须等 Run A 已冻结后再开。

只上传：

1. `ROLE-P1-2022C_RUN_B_ARCHITECT_REVIEWER_v0.2.zip`
2. 完全相同的官方5文件。

禁止给 B：

- A 输出；
- A 分数；
- A 方法；
- A first-fail；
- Run C prompt。

Run B 预算与 A 相同：最多40 tool calls、目标60分钟、最多一次 repair。

流程：

```text
Architect
→ FREEZE
Reviewer
→ FREEZE first-fail/audit
→ at most one Architect repair
→ Reviewer retest
→ FREEZE
```

## Chat C — Blind evaluator

必须等 A 和 B 都冻结。

先把 A/B 两个 bundle 随机改名为 X / Y，并在 C 冻结前不公开映射。

上传：

1. `ROLE-P1-2022C_RUN_C_BLIND_EVALUATOR_v0.2.zip`
2. 官方5文件；
3. anonymous bundle X；
4. anonymous bundle Y；
5. filled experiment registry / isolation metadata。

C 结束必须出现：

```text
BLIND_EVALUATION_FROZEN
```

只有之后才能揭盲 X/Y。

---

# 9. Blind evaluator 12项固定量表

每项 0–3：

1. problem-contract correctness
2. model-selection justification
3. six-hour baseline quality
4. assumption/constraint correctness
5. leakage prevention
6. mathematical validity
7. implementation feasibility
8. validation design
9. evidence provenance
10. error detection
11. repair quality
12. reproducibility

同时记录：

- first-pass material defects；
- defects caught before final freeze；
- unresolved blockers；
- fabricated/unreproduced numbers；
- tool/runtime failures；
- repair cycle count；
- hard failures。

不得仅凭写作风格选赢家。

---

# 10. 角色效果的 claim gate

完成一个 2022-C clean paired run 后，最多只允许写：

```text
ROLE_SPECIALIZATION_PILOT_EVIDENCE_POSITIVE
ROLE_SPECIALIZATION_PILOT_EVIDENCE_NEUTRAL
ROLE_SPECIALIZATION_PILOT_EVIDENCE_MIXED
ROLE_SPECIALIZATION_PILOT_EVIDENCE_NEGATIVE
```

单一 fixture **不能**升级成：

```text
ROLE_SPECIALIZATION_IMPROVES_CAPABILITY
```

要建立更强 claim，必须再做多题 held-out replication。

---

# 11. 未来发展路线

## Phase 1 — 完成 2022-C clean A/B/C

顺序：

```text
Run A
→ freeze
Run B
→ freeze
anonymize X/Y
→ Blind C
→ freeze
unblind
→ criterion-level delta analysis
```

## Phase 2 — Post-freeze 2022-C reference review

只有 A/B/C 全部冻结后，才允许读取 2022-C 优秀论文或外部答案。

作用：

- 查找 A/B 都漏掉的错误；
- 评价方法覆盖；
- 做 gap analysis；
- 不 retroactively 修改 blind score；
- 所有 post-freeze correction 必须标 provenance。

## Phase 3 — Role replication

至少再选若干 genuinely held-out fixtures，重复同样 A/B/C。

目标不是“赢一题”，而是观察：

- first-pass error 是否稳定减少；
- Reviewer 是否稳定发现实质错误；
- repair 后的数学/代码一致性是否提高；
- 额外角色成本是否值得。

## Phase 4 — Controlled Core Ablation

另开严格独立实验：

```text
No-Core
vs
Previous-Core (v1.40)
vs
New-Core (v1.41)
```

必须：

- 同题；
- 同预算；
- 同工具；
- 同 evaluator；
- 同 prompt contract；
- blind evaluation。

它回答的是 Core 训练是否带来 causal gain，与 Role Pilot 是两个不同问题。

## Phase 5 — 最终架构决策

只有 Role replication + Core Ablation 都有足够证据后，再决定：

- 是否将 Architect/Reviewer 作为生产接口；
- 是否保留 single-Core default；
- 哪些题型触发 Reviewer；
- 是否增加 Engineer / Writer 等角色接口。

无论如何，当前原则仍是：

```text
ONE SHARED CORE
NO DUPLICATED KNOWLEDGE BASE
```

---

# 12. 2025-D Test

2025-D 仍保留，不应为了当前 role pilot 提前消耗。

不要因为需要“再找一题”就打开2025-D答案/优秀论文。

---

# 13. 当前精确状态快照

```text
MathModel-Core v1.41.0 = SEALED
Core identity = VERIFIED

2023-C independent solve = FROZEN
2023-C post-freeze evidence = SEALED
2023 A/B/D/E/F excellent-paper exposure = PROHIBITED

2022-D role smoke = FROZEN
Q1 optimum = 54
Q2-C1 optimum = 40
Q2-C2 optimum = 40
Reviewer B = PASS scoped smoke

ROLE_SPECIALIZATION_IMPROVES_CAPABILITY = NOT_ESTABLISHED
CONTROLLED_CORE_ABLATION = NOT_RUN

2022-C source = FROZEN
2022-C Run A = NOT_RUN
2022-C Run B = NOT_RUN
2022-C Blind C = NOT_RUN

NEXT EXPERIMENT ACTION = FRESH CHAT A
```

---

# 14. 新的“项目总控 Chat”应该做什么

如果只是因为当前 Chat 太长，需要新建一个**总控 Chat**，请不要上传2022-C官方题面和数据。

总控 Chat 只需要：

1. `MathModel-Core_新Chat总交接_20260921.md`
2. `NEW_ORCHESTRATION_CHAT_FIRST_PROMPT.txt`
3. 可选：`ROLE-P1-2022C_ORCHESTRATION_TEXT_PACK_v0.2.zip`
4. 可选：`Graduate-MathModel-Learning-Skill-v1.41.release.json`

它负责：

- 维护实验 registry；
- 检查 A/B/C 是否按隔离协议完成；
- 回收 A bundle；
- 回收 B bundle；
- 匿名 X/Y；
- 在 C 冻结后揭盲；
- 做 criterion-level 差异分析；
- 决定是否进入 replication / ablation。

**它不负责解2022-C。**

---

# 15. 真正下一步：Fresh Chat A

如果用户现在就开始实验，则不要先建立另一个能看到完整历史的 Run A。

直接新建一个完全 fresh 的 Chat A，只给：

```text
ROLE-P1-2022C_RUN_A_SINGLE_CORE_v0.2.zip
2022C_官方题面_汽车制造公司涂装-总装缓存区调序调度优化问题.docx
2022C_附件1.xlsx
2022C_附件2.xlsx
2022C_附件3.xlsx
2022C_附件4.xlsx
```

然后粘贴本交接包内：

```text
RUN_A_FIRST_PROMPT.txt
```

这才是下一次真正的 capability experiment。

---

# 16. 最容易犯的错误

1. 在当前/总控 Chat 里直接解2022-C。
2. A 和 B 在同一 Chat 运行。
3. 给 B 看 A 输出。
4. 提前打开2022-C优秀论文。
5. 用2022-D smoke PASS 宣称 role superiority。
6. 把 heuristic timeout 当 infeasible proof。
7. 丢掉 Reviewer first-fail。
8. 因复杂模型“看起来高级”自动升级主线。
9. 未复现的数字写成 headline result。
10. 把 v0.1 run pack 与 v0.2 混用；正式使用 v0.2。

---

# 17. 换 Chat 后的优先级

```text
Priority 1: 保持2022-C blind isolation
Priority 2: 完成 Run A 并冻结
Priority 3: 独立 Run B 并冻结
Priority 4: Blind C
Priority 5: unblind + pilot evidence
Priority 6: held-out replication
Priority 7: Controlled Core Ablation
```

不要回退去继续优化2022-D，也不要继续读取2023-C。
