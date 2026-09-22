---
name: "modeling-paper-rubric-and-model-selector"
description: "按常见评分点生成建模论文结构与写作清单，并根据题目类型与数据条件给出模型选择与对照实验路线。Invoke when需要“论文格式/评分对齐/模型选型/路线不确定”。"
---

# 评分对齐论文结构与模型选型（Paper Rubric & Model Selector）

## 全局流程协作约束（长对话防漂移）

- 本 skill 不得作为孤立入口。用户要求完整论文、生成 Word、继续流程或不确定阶段时，先回到 `paper-workflow-orchestrator` 判断当前 S0-S8 阶段。
- 启动或继续本 skill 的正式任务前，必须运行：
  ```bash
  python .agents/skills/paper-workflow-orchestrator/scripts/workflow_guard.py --skill modeling-paper-rubric-and-model-selector
  ```
- 如果输出 `[WORKFLOW FAIL]` 或报告 `status != "PASS"`，停止本 skill，按 `paper_output/qa/workflow_guard_report.json` 的失败项回补前置阶段，不得凭记忆继续。
- 本 skill 只写入自己契约范围内的 `paper_output/` 产物；完成后必须回到 `paper-workflow-orchestrator` 判断下一步，并用 `context-memory-keeper` 记录已完成产物、阻塞项和下一步。
- 长对话中如果上下文变长、阶段不确定或用户分开调用 skill，先运行：
  ```bash
  python .agents/skills/paper-workflow-orchestrator/scripts/workflow_guard.py --status
  ```
  再读取 `paper_output/qa/workflow_guard_report.json`、`paper_output/preflight_report.json`、`paper_output/input_manifest.json`、`paper_output/results/run_manifest.json` 和本 skill 的上游 JSON 契约，按报告里的 `recommended_skill` 与 `next_action` 继续。
- 继续流程前，必须把 `paper_output/context/workflow_memory.json` 视为长期断点记录；若其中的 `current_step`、`next_step`、`recommended_skill` 与 `workflow_guard.py --status` 不一致，以 guard 报告为准。
- 每次完成本 skill 的产物后，先回到 `paper-workflow-orchestrator` 或运行 `workflow_guard.py --status`，再更新 workflow memory：
  ```bash
  python .agents/skills/context-memory-keeper/scripts/update_workflow_memory.py
  ```
  更新后读取 `paper_output/context/workflow_memory.json` / `.md`，确认下一步和推荐 skill 已记录。

## 执行契约
- 上游输入：优先读取 `paper_output/step1/problem_analysis.json`。
- 必须输出：`paper_output/plan/model_route.json`、`rubric_alignment.json`、`scoring_strategy.md`。
- 下游交接：数据、建模与证据门禁读取模型路线；S7 的 `paper-formal-writer` 将模型、验证和评分字段写入正式写作计划。`tasks.json` 仅供 legacy/quickstart。
- 推荐下一步：若需要外部数据，进入 `authoritative-data-harvester`；否则进入 `data-cleaning-and-visualization`。完整论文目标应回到 `paper-workflow-orchestrator` 判断后续阶段。
- 失败回退：若 `problem_analysis.json` 缺失，先运行 `problem-doc-model-selector`；完整 workflow 中本步骤失败时，QA 应回退到 `problem_analysis.json`。

## 目标
把“能拿分”的写作结构与“贴题可落地”的模型选型融合成一套可复用流程，输出：
- 一份可直接套用的论文大纲（按题目问法定制）
- 评分点对齐表（每个评分点对应你论文中的证据位置）
- 模型选型与对照实验路线（含基线、改进、验证与解释）

## 何时调用
- 需要快速搭建符合评分标准的论文结构与写作顺序
- 不确定模型是否贴题、是否过度复杂或解释不足
- 已有方案但担心“答非所问/指标口径不对/验证不充分”

## 输入（尽量提供）
- 比赛名称/年份/题号（可选）
- 题面原文或关键要求（必须）
- 你对每问的理解（可选，但强烈建议）
- 数据情况：来源、字段、时间跨度、样本量、缺失比例（可选）
- 约束与输出：需要预测/优化/评价/分类/聚类/仿真/调度等（必须）
- 你想强调的亮点：创新点/可解释性/可复现性（可选）

## 输入契约（推荐）
执行前优先读取：

- `paper_output/step1/problem_analysis.json`

如果该文件存在，必须以其中的 `questions[]` 作为唯一子问题来源，不得自行臆造、合并或丢弃子问题。

## 输出契约（推荐）
本 skill 应生成：

- `paper_output/plan/model_route.json`：每一问的模型路线、验证计划、图表证据与章节落点。
- `paper_output/plan/rubric_alignment.json`：评分点、证据形式和 QA 规则映射。
- `paper_output/plan/scoring_strategy.md`：给人和 Agent 阅读的评分闭环说明。

这些 JSON 是项目自定义 workflow contracts，不是平台内置标准。详细规则见 `docs/workflow-contracts.md`。

## 脚本入口（推荐）
```bash
python .agents/skills/modeling-paper-rubric-and-model-selector/scripts/build_model_route.py
```

该脚本会读取 `paper_output/step1/problem_analysis.json`，并将模型路线与评分闭环写入 `paper_output/plan/`。若该文件不存在，应先运行 `problem-doc-model-selector`。

## 外部“论文结构提示词”资源（可选）
支持把你预先准备的论文结构提示词文件（或文本）附加到本技能中，用于生成与评估。

### 分层目录约定（推荐）
- `SKILL.md`：技能定义与用法说明
- `references/`：可复用的参考材料与提示词资源（默认模板、评分点清单等）

### 使用方式（任选其一）
1) 路径引用（推荐）
- 在调用时提供：`paper_prompt_path`
- 规则：若提供该路径，则优先读取其内容作为“论文结构提示词”；若未提供，则使用本技能自带的默认提示词文件。

2) 直接粘贴
- 在调用时提供：`paper_prompt_text`
- 规则：若提供该文本，则优先使用该文本；否则使用 `paper_prompt_path`；若两者都没有，则使用默认提示词文件。

### 调用示例
- 方式1（路径）：
  - `paper_prompt_path: <项目根目录>\paper_output\plan\paper_prompt.md`
- 方式2（粘贴）：
  - `paper_prompt_text: <把你的论文结构提示词全文粘贴在这里>`

### 运行时整合机制（推荐参考）
在生成 A/B/C/D 任一产出前，**建议读取** `references/paper_prompt_default.md` 作为“结构参考”：
1. **参考优先级**：此文件作为写作模板的参考，但**不强制阻塞**生成。生成的论文大纲应尽量对应此文件的章节要求，但允许模型根据实际语境发挥。
2. **防遗忘机制**：
   - 建议在 Prompt 中提及此文件的核心结构（如六段式摘要），引导模型生成。
   - 若用户提供了额外的 prompt，则以用户的要求为主，此文件为辅。
3. **鼓励扩写**：在保证逻辑通顺的前提下，**鼓励**使用学术化的“万金油”语句（如“随着…的发展”、“综上所述”）来丰富篇幅，增强文章的连贯性与体量感。

然后把 `PAPER_PROMPT` 作为强约束与写作风格来源，融入到：
- 论文大纲的章节命名、写作顺序、字数分配与语体要求
- 评分点对齐表中的“证据形态”（哪些图、哪些表、哪些检验）
- 模型路线与对照实验设计（尤其是“模型检验/鲁棒性/敏感性/可复现”要求）

### 向后兼容
不提供 `paper_prompt_path` / `paper_prompt_text` 时，本技能维持原有默认行为正常输出。

## 约束（必须遵守）

- **Memory Interaction (必做)**:
  - **开始前**，检查 `memoryskill.md` 中的 `External Resources / Literature`，若存在相关文献，必须将其融入“参考文献”章节及“模型建立”部分的背景综述中。
  - **完成后**，将生成的“论文大纲”与“模型路线”更新至 `memoryskill.md`。

## 产出（固定结构）
### A. 一页纸题意对齐
- 每一问：输入、输出、评价指标、关键约束、边界条件、可行验证方式

### B. 论文大纲（按评分友好顺序）
必须包含并按题目调整比重：
1. 摘要（中英文按要求）：问题、方法、结果、贡献、关键词
2. 问题重述：用你自己的话把每问变成可计算任务
3. 模型假设：必要且可辩护，逐条说明合理性与影响
4. 符号与变量说明：表格化，含单位与范围
5. 数据说明与预处理：来源、清洗规则、缺失/异常处理、可复现步骤
6. 模型建立（按问分小节）：目标函数/约束/损失、推导或结构说明
7. 求解方法与实现：算法步骤、复杂度/收敛、参数设置
8. 结果与分析：主结果、可视化、对比、误差/收益解释
9. 模型检验：对照实验、敏感性分析、鲁棒性测试、极端情景
10. 结论与建议：对应每问给结论与可执行建议
11. 不足与展望：诚实但不自毁，指出改进方向
12. 参考文献：规范引用题面、数据源与关键方法
13. 附录：关键代码、额外图表、符号补充（按比赛要求取舍）

### C. 评分点对齐表（以“证据”为核心）
输出一张表：评分点 → 你提供的证据 → 论文位置（章节/图表/表格/实验）。
常见评分点映射（按比赛可增删）：
- 题意理解准确：一页纸题意对齐 + 问题重述逐问可计算
- 模型合理性：目标/约束与题面一致，假设可辩护
- 方法创新/改进：在基线之上有明确改进点，并说明为何有效
- 结果可信：有验证、有对比、有误差分析或约束满足证明
- 表达清晰：符号统一、图表自解释、结论逐问对应
- 可复现：数据来源与处理、参数设置、算法步骤完整

### D. 模型选型与路线（先贴题再高级）
对每一问输出：
- 任务类型判定：预测/分类/聚类/评价/优化/仿真/机理建模
- 最小可用基线：能跑通、可解释、可对照
- 一到两条改进路线：提升精度/鲁棒/效率/解释
- 验证计划：指标、交叉验证/留出法/回测、消融、敏感性
- 风险点：数据不足、口径不一、过拟合、不可解释、计算超时

## 模型选型速查（按题目常见问法）
### 1) 预测类（时间序列/回归）
适用：给定历史，预测未来或估计参数。
- 基线：移动平均/指数平滑/线性回归/ARIMA（能解释趋势与季节）
- 改进：特征工程 + 树模型；或 LSTM/Transformer（样本量足够再上）
- 验证：滚动回测、MAPE/RMSE、置信区间/误差分解

### 2) 分类/判别
适用：判定类别、风险等级、是否发生。
- 基线：逻辑回归/朴素贝叶斯（可解释）
- 改进：随机森林/梯度提升；代价敏感学习（类别不平衡）
- 验证：AUC/F1/PR 曲线、混淆矩阵、阈值敏感性

### 3) 评价/排序/综合指数
适用：多指标打分、排序、择优。
- 基线：规范化 + 加权和（权重可来自题面或专家）
- 改进：熵权/CRITIC/AHP/TOPSIS/VIKOR（明确权重来源与意义）
- 验证：权重敏感性、排名稳定性、与已知事实对照

### 4) 优化/调度/选址/路径
适用：资源分配、成本最小/收益最大、满足约束。
- 基线：线性规划/整数规划（目标与约束写清楚）
- 改进：多目标（加权/ε-约束）、启发式（遗传/模拟退火）用于大规模
- 验证：可行性检查、对照基准策略、约束违背率、复杂度与时间

### 5) 聚类/分群/画像
适用：无标签分组、模式发现。
- 基线：K-means/层次聚类
- 改进：GMM/DBSCAN（噪声与形状复杂时）
- 验证：轮廓系数/稳定性、可解释的群体差异描述

### 6) 机理/仿真/系统动力学
适用：强调机制解释、情景推演。
- 基线：微分方程/差分方程/系统动力学
- 改进：参数校准 + 不确定性分析；与数据驱动模型对照
- 验证：历史拟合、情景一致性、参数敏感性

## 防跑偏硬规则（必须检查）
- 每一问至少给出一个“可量化输出”和一个“可验证指标/检验方式”
- 模型中的每个关键变量都能在题面/数据里找到定义与单位
- 图表和结论逐问对应，不出现“做了很多但没回答问题”
- 至少一个基线对照：证明你的方法相对简单方案有提升或更合理

## 最终交付（你需要让我生成时，我会给出）
- 可直接粘到论文里的大纲与小节标题（按题目问法编号）
- 评分点对齐表（含你该补的图表/实验清单）
- 每问模型路线：基线 + 改进 + 验证 + 风险与备选

## 默认提示词文件（可复用）
当未提供 `paper_prompt_path` / `paper_prompt_text` 时，默认从以下文件读取论文结构提示词：
- `references/paper_prompt_default.md`

## 目录约定（与项目全局对齐）
- 赛题与附件统一放在 `problem_files/`，补充数据放在 `crawled_data/`。
- 建议把本技能的输出（大纲/评分点对齐/模型路线）归档到 `paper_output/plan/`，供后续生成正文时引用。
- 上面的 `paper_prompts/...` 仅为历史路径示例；当前项目推荐把自定义提示词文件也归档到 `paper_output/plan/`，或直接使用本技能自带的 `references/paper_prompt_default.md`。

## 前后衔接
- 前置：无（拿到题面就能用）。
- 后续：`problem-doc-model-selector`（更细的逐问解析）或回到 `paper-workflow-orchestrator` 继续论文 workflow。

## 约束（必须遵守）

- **Memory Interaction (必做)**:
  - **完成规划后**，必须调用 `context-memory-keeper`，将“论文大纲结构”、“核心评分点”更新到 `memoryskill.md`。
- 本技能必须输出“评分点 → 证据 → 论文位置”的映射清单；后续产文时必须能逐条落到具体章节/图表/表格，否则视为未对齐。
- 若输出中要求“数据预处理/可视化证据”，后续必须调用 `data-cleaning-and-visualization` 产出 `paper_output/figures/`，否则该评分点缺证据。
- 若用户目标是“论文生产完整”，本技能结束后必须明确下一步：进入数据/图表阶段，或回到 `paper-workflow-orchestrator` 继续完整 workflow。


## 级联/stacking 与不平衡分类的选择闸门

- 任何两阶段/stacking/cascade 路线，在评分前先回答：第二阶段训练时收到的是 oracle 中间量还是第一阶段预测量？若线上是预测量，训练必须用 OOF/cross-fit 中间预测。
- 类别不平衡优先比较 class_weight、balanced loss 与 training-fold-only resampling；禁止全数据过采样后再切分。
- TargetEncoder 等监督编码纳入模型本身，必须在 CV fold 内拟合；不能作为 split 前“数据清洗”。
- 中间物理量到结构化标签存在多对一时，优先直接联合标签建模或输出候选分布，不把不可逆映射强行反演。

## 结构化分类与不平衡指标闸门（v1.15）

- 对 `(MCS,NSS)`、多部件状态、层级标签等结构化输出，先列合法 tuple 集；独立多头必须增加约束解码和 joint exact-match/invalid-pair 指标，不能只报每个头的 Accuracy。
- 只要 Accuracy 与 macro F1/少数类 Recall 明显背离，模型选择以 macro/balanced/per-class 证据为主，并绘制 support-aware confusion/metric dashboard。
- 物理功率特征出现 dBm/RSSI 时，先审量纲与聚合规则；任何直接 dBm 求和作为功率和的方案不得进入候选主线。
- 摘要、结果表、结论段的数值由同一结果 registry 生成；手工重复录入的核心指标在终稿前必须自动比对。

## 时序模型与指标代数闸门（v1.16）

- RNN/LSTM 候选必须展示输入 tensor 的真实 `T` 维及其时间/实体语义；`T=1` 自动降级为“非时序深层模型”，需要与 MLP/树模型公平比较。
- 模型排名前自动运行指标代数 sanity check；MSE/MAE、RMSE/MSE、百分比、概率、混淆矩阵派生指标有矛盾时先修结果，禁止继续选模。
- 有明确机理公式可直接给出目标近似时，它是强制基线；机器学习应解释是在校正残差、补充未建模效应还是替代不可观测量。

## 物理-数据混合与优化可行性闸门（v1.17）

- 波形/高维信号先定义一份 train/inference 共用特征 schema；任何模型比较前先通过 schema contract。
- 因素主效应/交互分析如果存在频率、幅值、剂量、暴露等连续强驱动变量，默认用 ANCOVA/稳健回归调整，再比较效应量；不以原始均值 ANOVA 的 p 值直接排序“影响程度”。
- 机理参数拟合后生成唯一 parameter registry；预测、图表、公式和优化全部引用该 registry，避免手工抄参。
- 跨工况“泛化”最低要求是 grouped / leave-condition-out 验证；训练集拟合优度只能做校准证据。
- 优化模型选型前必须先过四关：目标完整、变量完整、可行域完整、代理模型支持域完整。报告的最优点逐一 replay 约束；不可行点不进入论文。
- 多目标没有明确偏好时默认保留 Pareto/ε-constraint；比值法或加权和只能作为声明了偏好后的选点策略，而不是替代整个多目标结构。

## 泛化单位与混合优化编码闸门（v1.18）

- 模型选择前先写“将来真正未见的单位是什么”；温度/材料/设备/患者/站点/会话等若是部署泛化维度，CV 必须按该单位分组留出，随机行 KFold 只能当插值证据。
- `p>0.05` 不作为“独立/无作用”的正面证据；比较效应值和区间，必要时做等效性检验。
- 特征 contract 包含变换和 dtype；paper/code/train/inference 中 raw/log/normalized 或 id/string 不一致时，候选模型先淘汰或修复。
- 论文最终组合模型必须能从原始输入一路运行到最终输出；只验证一个 ablation 不能代表最终 stacking/physics+ML 管线。
- 多目标加权前先审单位和尺度；未经归一化的“1:1 权重”不解释为等偏好。无偏好来源时保留 Pareto/ε-constraint。
- 混合离散优化对每个类别做 encoder round-trip 单元测试，并要求所有比较优化器使用同一目标、约束和计算预算的多 seed 分布证据。

## 特征链与多目标尺度闸门（v1.18）

- 对任何“特征增强/物理先验/模型堆叠”方案，模型选择前先生成一份最终 `feature_contract`，并验证论文声称的每个特征都真正进入模型输入。
- 类别变量在训练、验证、推理、优化器调用四个阶段必须使用同一编码器；用全部合法类别做 round-trip/非零编码烟测。
- 若任务要求“通用模型”，随机行留出只能作为基础分数；模型排序必须加入跨材料/跨温度/跨工况的分组验证。
- 多目标优化不接受未归一化的“1:1 就代表同等重要”解释；优先 Pareto/epsilon-constraint，或至少给出目标尺度与权重敏感性。
- 自定义指标必须登记公式、单位/无量纲、值域和优化方向；若名称与公式方向冲突，先修正指标语义再排名。

## 交互、架构与 Pareto 真实性闸门（v1.19）

- 候选方案写“交互/协同”前必须有显式 interaction term；交叉分组均值只能当描述性探索，连续强驱动量必须先调整。
- 深度模型按 executable layer graph 选型，不按论文标题选型；Bi-LSTM/attention 等组件必须真实实例化并接入 forward 路径，输入 shape/sequence 语义必须匹配。
- 随机扰动测试只记为 perturbation robustness；跨工况泛化的模型排名只看对应 group/condition 的真正留出结果。
- 多目标偏好权重是外部决策参数，不作为自由优化变量；没有偏好时保留 Pareto front，再用 knee/utility/epsilon 等规则选点。
- Pareto 优化器比较采用统一预算、多 seed、HV/IGD/spread/feasible-rate；“点更密”或单次前沿更好看不能决定模型/算法排名。
- 所有论文报告的最优/Pareto 点必须用最终代理模型、同一 encoder 和同一 bounds 逐点 replay；越界或目标无法复算时先修结果再写结论。

## 效应量、多重比较与混合优化真实性闸门（v1.20）

- 因素分析候选方案若只用 F/p-value 排“影响程度”，先降级；模型选择优先统一调整模型中的效应量、contrast、CI，并控制频率/幅值等连续混杂。
- 多次 pairwise test 必须先定义 family，再做 Holm/FDR/Bonferroni 或 global-test + corrected post-hoc；未经校正的序贯显著性淘汰不用于最终条件选择。
- “找最优组”的逐对擂台算法要测试组顺序敏感性；若换顺序会换 winner，则不得作为唯一优化依据。
- 混合整数/类别优化必须使用合法离散集合；普通连续 PSO/GA 若产生 37.4°C、材料1.6 之类点，除非有明确 repair/decoder，否则视为不可行。
- paper、code、result table 的可行域从同一 domain registry 生成；任何变量出现 5000/50000 一类边界分叉，先修 registry 再跑优化。
- 标量化结果进入模型选择前必须 replay：用报告的子目标值和权重重算总目标。lambda 行/标签无法重算时，不比较算法优劣、不选最终点。
- 深度自表示/物理融合模型可以作为增强模型，但最终排序以 deployment-relevant grouped/leave-condition-out 结果为准；随机行 80/20 高分只做插值基准。

## 时序、物理单位与干预决策闸门（v1.21）

- 时间序列候选先审“泛化到未来”的验证单位：split/group first，再在折内构造窗口；高度重叠窗口随机切分的高 R² 不用于模型排名。
- 任何交通/物理代理量进入机理公式前先审单位和标定。相对密度、像素距离、归一化速度若没有物理尺度映射，不以 km/h、veh/km 等物理输出参与控制阈值。
- 预测型模型与控制型模型分层评分：预测准确不自动证明“执行某动作会改善结果”。控制方案必须单独给 counterfactual/intervention evidence。
- 相关性热图仅作为结构探索；要推荐应急车道开放、治疗、调度、策略等干预动作，优先真实干预数据、可信仿真或因果设计，并给不确定性。
- 人工倍率产生的“干预后曲线”只能记为情景假设，不能作为模型收益指标。敏感性分析必须覆盖倍率范围与结论稳定性。
- 事件预测/预警模型以事件级 precision/recall、误报率、漏报率、提前量/延迟量为主；只展示命中的几个案例不进入最终模型优选证据。
- 所有守恒/状态递推公式先做量纲单元测试和极限条件测试；量纲不闭合的模型不得进入优化与部署候选。


## 交通视频、阈值策略与布点优化闸门（v1.22）

- 视频交通模型先登记 FPS、frame stride、aggregation window；速度/流量/密度只使用能从该时间基准和空间标定重算的物理量。
- 将 unique passage count、occupancy、flow、density 分开建变量；未标定的相对密度不得直接进入 Greenberg 等物理模型输出 km/h。
- RNN/GRU/LSTM 候选必须 `T>1` 且时间顺序/组边界明确；attention/multi-head 等组件按可执行层图核验，不按论文命名选择。
- 预警/控制阈值必须来自一份 state-machine registry，显式处理灰区、滞回、最短保持时间与 OR/AND 逻辑。
- 分布拟合/MLE 只有在“拟合参数 → 分位数/风险函数 → 业务阈值”可回放时才计入阈值证据。
- 跨监测点迁移干预效果时，将 transportability 作为独立验证任务；未经验证的 transferred counterfactual 不进入最终收益排名。
- 传感器/摄像头布点优化的变量必须直接编码位置、数量、类型等交付量；并要求 sensing→estimation→decision→outcome 中介链后才评价交通收益。
- 模型/方案排序前统一 replay RMSE/MSE、百分比变化和优化可行性，数值表存在硬矛盾时先修表再比较。


## 交通库存预测与传感器依赖闸门（v1.23）

- `q-rho-u` 候选模型先过单位闭合；veh/min 与 km/h 不允许直接代入 `q=rho*u` 后不换算。
- 提前预测模型必须给 chronological/grouped split 证据；平滑趋势相关性不能替代真正 ahead holdout。
- 库存型控制器优先保留开/关滞回，但 Qmax、jam/critical/alarm thresholds 必须分开校准并做敏感性。
- 任何“开放后提升30%”等固定倍率模型降级为 scenario，模型排名不使用其单点收益，除非倍率来自观测干预/可信仿真。
- 传感器布局变化时自动重建 feature-to-sensor dependency graph；关键策略输入失去观测能力的方案先淘汰或重新设计控制器。
- 只列附录文件名、不提供源码的方案不获得“实现完整”加分；论文公式可 replay，但代码可运行性保持 unknown。


## 公式回放、控制状态与情景干预闸门（v1.23）

- 关键推导式必须能从上一式代数反解并用一行真实数据回放；推导/回归方程尺度不一致时，候选模型先降级。
- 时序预测的 split 方式必须明确到 chronological/grouped/random；部署面向未来时，随机行 70/30 不作为主验证。
- 守恒型 `K(t)` 状态可以优先候选，但 Q0/Qmax、积分步长、阈值/滞回和权重都要校准并做敏感性。
- 任何固定倍率生成的“干预后”结果只计入 scenario evidence，不计入真实 treatment benefit。
- 传感器布点题必须比较可执行的坐标/数量/成本方案；只有定性搬迁建议不进入“优化模型”排名。
- 附录仅列文件名时，不把算法标记为已实现/已复现；模型选择只使用论文可复算证据与可见代码证据。


## 目标泄漏、最差组与反事实自洽闸门（v1.24）

- 候选预测模型进入比较前先做 feature-target identity / deterministic-copy 检查；一旦泄漏，禁止用其验证分数参与选模。
- RNN/TCN/LSTM/BiGRU 必须报告真实序列长度 T、窗口跨度和预测 horizon；T=1 不获得“时序模型”加分。
- 论文声称的 SK-Net/attention 等结构必须从真实计算图核验，名称本身不作为复杂模型优势。
- 多站点/视频/工况模型按 worst-group metric 排雷，再看平均指标；负 R² 子组不得被平均高分遮蔽。
- 机理反事实方案必须逐点满足治理方程和单位约束；手工倍率默认属于敏感性情景，不作为因果收益。
- 摄像头/传感器布点只有在变量、可行域、目标、成本与基线都显式时才进入“优化模型”候选。
