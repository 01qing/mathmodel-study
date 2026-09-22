# Graduate-MathModel-Learning-Skill v1.20 进度

## 本版范围

v1.20 在 v1.19 基础上完成 2024-C 第四篇训练论文 S012（C24106130096，《多变量复杂环境下的磁芯损耗建模》）的核心全文精读，并将 S009-S012 四篇闭环为同题方法族。

本版的“训练”继续指 Skill 规则、案例库、代码审计库、图表论证模板与检索能力的增量学习，不修改基础模型参数。

## S012 阅读/代码状态

- 物理页：105/105 全文文本已读并逐问拆解。
- 附录：打印 Python Listing 2-7 已做静态代码审计。
- 精确烟测：完成 Q1 数据切分/预处理 contract 检查，以及 Q5 约束与标量化结果 exact replay。
- 原作者端到端复现：**未完成**。当前工作区缺官方 2024-C 原始附件、若干派生特征文件和确定性模型检查点，因此不宣称作者全链已运行。
- 像素级论文版式/配色：**未完成**。当前工作树只有全文提取层，不宣称已经学习 S012 原 PDF 的颜色、字体和像素布局。

## 逐问新增知识

### Q1 波形分类

可学习路线：形状阈值基线 → 5维时域统计特征 SVM → 单 SNR 噪声压力测试 → Hilbert-Huang + 双谱多域特征。

代码审计发现：
- `get_feature()` 在完整特征矩阵上先计算 feature-wise min/max，再进入 `train_test_split`；
- `data_10` 与 `data_snr_10` 也先按列 Min-Max，再切分；
- 因此验证集极值进入预处理统计量。

新门禁：所有跨样本 scaler/feature selector/PCA 必须 split/group first 后只 fit 训练折。逐样本自身归一化与跨样本缩放需要区分。

### Q2 Steinmetz 修正

论文形成 SE → LSE → TLSE → TLSEDSR 的完整假设梯子，且打印附录确有 NAdam/自表示网络实现证据。这是 S012 值得优先借鉴的部分。

风险：关键评价仍是同材料/同波形支持内随机 80/20 行切分，`R²≈1/MRE≈0.12` 只能说明插值性能；新题若声称跨温度/跨材料，应使用 leave-temperature/leave-condition-out。

### Q3 因素与交互

优点：S012 真正写出三因素模型及两两 interaction term，比只看交叉分组均值更严谨。

新增审计发现：
- 表5.19温度行 F=17.755，但正文误把截距行 F=3456.213 当成温度 F；
- 后续把不同单因素模型的 F 直接解释为“影响程度”排序，F 不是跨模型可直接比较的效应量；
- 47 次 Mann-Whitney 序贯比较未见 FWER/FDR 校正；
- “当前优胜组 vs 下一组”淘汰流程具有组顺序依赖风险。

新增规则：effect size/CI、多重比较校正、序贯淘汰顺序不变性测试。

### Q4 通用磁芯损耗预测

DM/DMSDR/TDM → LMSE/LMSESDR → TLMSESDR → MTLMSESDR → WMTLMSEDSR 构成很好的 ablation ladder；打印代码也能看到 material/waveform Embedding，最终方法的实现证据强于 S010/S011 的若干“论文名—代码链”缺口。

但随机行切分仍不能证明跨材料/温度/波形/频率区间泛化。新 Skill 将“ablation ladder”与“leave-condition-out”绑定使用。

### Q5 多目标优化

精确复核发现：
1. 论文数学约束：`f ∈ [50000,500000]`；GA/PSO 打印代码：`lb=[5000,...]`。
2. 论文报告 PSO `λ=1` 点 `f=7862.85`：在代码域内可行，在论文模型域内不可行。
3. 温度理论上仅 `{25,50,70,90}`，材料/波形是离散类别；代码却使用连续 box 搜索。
4. 按 `L=P_loss-λ*energy` exact replay：λ=0.01/0.1/1 行可复算；标为 λ=10 的行隐含 λ≈100，标为 λ=100 的行隐含 λ≈10，存在结果行/标签漂移。
5. 打印脚本 `Lambda=[0.01,0.1,1,10,100][4]` 实际固定为100，不会在一次未改代码运行中生成整张 λ 扫描表。

新增规则：machine-readable domain registry、mixed-variable discrete feasibility、结果表 objective replay、run-config/lambda/seed/budget registry。

## 2024-C 四篇最终组合路线

S009-S012 不按“哪一篇最好”投票，而按局部证据组合：

- Q1：可解释波形/形状基线 + 必要时多域特征；所有缩放/筛选在训练折内；group/condition stress test。
- Q2：物理 Steinmetz/log-linear 基线 + 温度修正；只有 leave-condition-out 稳定提升时才引入自适应参数网络。
- Q3：统一协变量调整的 factorial/ANCOVA/稳健模型 + 显式 interactions + effect size/CI + multiplicity-corrected post-hoc。
- Q4：固定 feature/schema 的 physics/empirical baseline + ablation ladder；按 leave-material/temperature/waveform/frequency-region 评价。
- Q5：一个 domain registry 管理连续/离散可行域；优先 Pareto/epsilon-constraint 或无量纲 scalarization；所有最终点做 exact feasibility + objective replay。

## 新增资产

- `knowledge_base/paper_reviews/2024-C-S012-core.json`
- `knowledge_base/code_cases/2024-C-S012-appendix-code.json`
- `knowledge_base/figure_argumentation/S012.json`
- `knowledge_base/cross_paper_maps/2024-C-S009-S012.json` 更新为四篇闭环
- `learning_output/analyses/v120_S012/contract_replay_smoke.json`
- `references/2024-C-S012-paper-code-audit.md`
- 6 个新增错误模式：F-as-effect-size、多重检验、序贯淘汰顺序依赖、混合变量连续松弛、paper/code边界漂移、标量化结果表不可复算
- 3 个代码绘图证据模板：effect-size+corrected-tests、domain feasibility、scalarized-objective replay

## 回归与冻结边界

- v1.20 S012 专项回归：60/60 PASS。
- 2024-C S012 真实检索烟测：PASS。
- v1.6 → v1.20 历史核心规则回归：已逐批复跑；历史“瞬时状态/固定版本号”断言已改为真正的向前兼容不变量。
- 2024-A、2024-B、2024-C、2025-E/教师代码相关历史检索/代码链回归：PASS（批次超时的项目已拆成单项复跑）。
- 论文库存：45。
- 检索片段：6752。
- 冻结划分：32 train / 7 dev / 6 test。
- 当前 reviewed：train S001-S012；dev 0；test 0。
- split manifest SHA256：`0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`，与冻结记录一致。

## 下一步

编号 S013-S016 属于 **dev split**，不直接作为训练论文吸收。下一篇训练论文应跳到 **S017 / 2024-E**。

开发组将在训练规则阶段性冻结后用于调参/误差分析；测试组继续执行“先冻结 Skill 独立完成，再打开测试论文对比”的协议。
