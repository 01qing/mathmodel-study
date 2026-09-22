# PROGRESS V1.26 — MathModel-Core / S026

## 版本定位

v1.26 继续单一共享 **MathModel-Core** 主线，不拆 Master / Architect / Engineer / Writer / Reviewer，不复制知识库。v1.25/S025 资产原样保留；本版本只增量学习 **S026 / 2025-A**。

## S026 学习范围

- split：train。
- 原 PDF：98 页。
- 全文：98/98 页精读。
- 视觉：98/98 页原 PDF contact-sheet 扫描，并抽查关键正文/结果页。视觉审查单独记录。
- 代码：打印 MATLAB Appendix A 静态审计。Q1/Q2 有长代码清单；Q3 DPEA 实现未在附录中出现。
- Reproduction Level：**R2**。缺作者原始 `.m`、完整输入 bundle 与 MATLAB 运行环境；Q3 实现缺失，因此不得提升 R3-R7。

## 新协议 10 步执行结果

1. **全文学习**：完成。
2. **代码/公式/图表审计**：完成，见 S026 paper/code/figure assets。
3. **Candidate Model Competition**：Q1-Q3 均建立 Baseline / 作者方案 / 主要替代 / 不推荐 / switch conditions。
4. **6小时 Baseline**：
   - Q1：Kahn ready-set + FREE-first + critical-path/slack。
   - Q2：lifetime sweep + Best-Fit + true incremental spill bytes / next-use victim。
   - Q3：epsilon-constraint hard transfer cap + resource-aware list scheduling/local search。
5. **可迁移模块**：feasible-neighborhood search、feasibility replay、event-driven runtime evaluator、dual-population concept（高风险）。
6. **错误模式**：新增 priority-feature drift、algorithm-defining primitives dead code、global-best state/score desync、cross-question objective drift、metaheuristic no matched-budget baseline。
7. **Reproduction Level**：R2。
8. **同题 Method Map**：S025-S026 已形成 provisional 两篇竞争图谱，S027/S028 尚未学习。
9. **Skill 规则**：新增 defining-primitives trace、结构化 tabu token、量纲不同目标不裸加、shared evaluator、hard-cap-before-Pareto 等 v1.26 门禁。
10. **专项回归**：68/68 PASS；2025-A S026 retrieval regression PASS。

## S026 关键审计结论

### Q1
- 正文优先级包含 Type + Size + Criticality；可见 greedy 代码只有粗粒度 Op-type score。
- 正文称 tabu length 动态调整；代码固定 `tabu_length=20`，动态的是 neighborhood size。
- tabu list 把 move 字符串拼成字符流再按字符长度截断，不是 move-level FIFO queue。
- Result Registry：S026 与 S025 在 5/6 workload 的 Q1 Cmax 相同；Conv_Case0 为 14592 vs 7660，S026 更差 6932。

### Q2
- `Mbest` 与 local attractor `P` 被计算但不参与后续 state update；可见更新更接近 inertia/c1/c2 PSO，不能仅凭名称认定真实 ABQPSO。
- `Bytes + 0.1*Cycles` 未归一化，主/次目标存在量纲尺度支配风险。
- local-search 改进 `globalBest` 对象但未同步 scalar `globalBestFitness`，存在 best-state/score desync。
- S026 报告 Q2 extra transfer 在六个 workload 上均高于 S025；在 shared evaluator 完成前，只能说“表值更高”，不能跨论文直接判优。

### Q3
- DPEA 可执行 Appendix 实现未见。
- Q2 与 Q3 的 SPILL/COPY_IN transfer 公式语义漂移，不能直接跨问计算 improvement。
- hard transfer tolerance 没有在 Pareto 前显式编码为 epsilon constraint。
- 表6.8相对 S026 Q2 的百分比算术基本自洽，但不能追溯到可执行 Q3 code。

## Figure Decision Rules 更新

2025-A 暂定核心证据组合扩展为：
- problem/decomposition diagram；
- Vstay/lifetime trajectory；
- stochastic optimizer convergence（多 seed + matched budget 更好）；
- cache utilization/composition；
- cache lifecycle Gantt；
- **真实 feasible Pareto scatter + hard-cap line + selected operating point**。

通用 Pareto 示意图或 radar before/after 不能代替真实非支配前沿。

## Method Composer / S025↔S026

当前 provisional 组合：

`共同 DAG/parser → 6小时 Q1 baseline（SA/Tabu 只作 matched-budget refiner） → S026 修复后的 feasibility + runtime evaluator → S025 lower-reported-transfer allocator candidate → Q3 epsilon-constraint`

需要 adapter 统一：node/buffer schema、SPILL/COPY_IN cost、生命周期、Bytes/Cycles 单位、容量/拓扑约束和 Result Registry。

当前阻断组件：
- S026 Q2 “ABQPSO quantum” 主线：defining primitives 未参与 update。
- S026 Q3 DPEA 主线：无可执行 appendix + transfer formula drift。

## 数据边界

- papers = 45
- chunks = 6752
- split = 32 train / 7 dev / 6 test
- S025/S026 = reviewed train
- S027/S028 = pending train
- S029/S030 = dev protected unread
- all test = protected unread

## Mini Transfer Test

**NOT_DUE_CASE_GROUP_INCOMPLETE**。2025-A Train 组必须先完成 S025-S028，再做题组级 Mini Transfer Test；当前不打开 dev/test 答案。

## 下一步

进入 **S027 / 2025-A**，继续相同 MathModel-Core 10步协议，并扩展 S025-S028 Same-Problem Method Competition Map。
