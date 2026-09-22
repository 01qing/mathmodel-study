# PROGRESS V1.25 — MathModel-Core protocol + S025

## 定位

从本版本起，兼容目录 `graduate-mathmodel-learning` 正式定位为 **MathModel-Core 核心知识 Skill**。当前不拆 Master / Architect / Engineer / Writer / Reviewer，不复制知识库。v1.24 / S020 已先按旧计划正式封存，S001-S020 未因新协议重读。

## S025 / 2025-A

- 原 PDF：59 页，已全文读取。
- 视觉：59/59 页 90dpi 联系表扫描 + 关键页 160dpi；视觉状态独立于代码复现等级。
- 附录：Q1.py / Q2.py / Q3.py 打印代码静态审计。
- Reproduction Level：**R2**。没有作者原始可执行 `.py` 与完整输入数据，不提升 R3-R7。
- 已建立 Q1-Q3 Candidate Model Competition 与 6 小时 Baseline。
- 已建立 `knowledge_base/result_registry/S025.json`，并复算 Q3 硬约束和改进率。
- 已建立 `knowledge_base/method_modules/2025-A-S025-modules.json` 和 Method Composer 七门兼容性合同。
- 已建立 2025-A provisional Figure Decision Rules。

## S025 关键审计结论

1. Q1 论文声称模拟退火，但打印 Q1.py 未看到 SA 主循环；图5.7视觉数值与相邻正文 14000→7760 存在合同漂移。
2. Q2 论文声称 ILP/CBC + rounding，打印 Q2.py 只见启发式分配/SPILL；offset=0 truthiness 与 reallocation None guard 存在风险。
3. Q2/Q3 同名 SPILL victim 策略方向漂移：Q2偏小 buffer，Q3/正文偏大 buffer。
4. Q3 表5.5 中 Conv_Case1、Matmul_Case1 违反 `C* <= 1.05*C_Q2`；仅 Matmul_Case0 改善执行时间。
5. Conv_Case0 表内 transfer improvement 符号错误，Result Registry 已自动捕获。

## 新协议资产

- `knowledge_base/core_schema/mathmodel_core_question_schema_v1.json`
- `knowledge_base/core_schema/reproduction_levels_v1.json`
- `knowledge_base/core_schema/result_registry_schema_v1.json`
- `knowledge_base/core_schema/method_composer_contract_v1.json`
- `knowledge_base/core_schema/figure_decision_rule_schema_v1.json`
- 非破坏迁移：`migrate_legacy_core_cards.py`，默认只报告旧卡缺字段，不自动重写。
- Result Registry 验证：`validate_result_registry.py`。
- Method Composer 合同检查：`check_method_composition.py`。

## 数据边界

- 论文总数：45
- chunks：6752
- split：32 train / 7 dev / 6 test
- 当前 reviewed：S001, S002, S003, S004, S005, S006, S007, S008, S009, S010, S011, S012, S017, S018, S019, S020, S025
- reviewed dev：[]
- reviewed test：[]
- split manifest SHA256：`0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`

S021-S024、S037-S038 测试组仍冻结；2025-A 的 Dev 也没有为了本轮测试提前打开。

## Mini Transfer Test

2025-A 题组尚未闭环：S025 已完成，S026-S028 待学。因此本版本状态为 **NOT_DUE_CASE_GROUP_INCOMPLETE**。题组闭环后再执行 Mini Transfer Test。

## 下一步

进入 **S026 / 2025-A**，继续按照 MathModel-Core v1.25+ 协议学习，并持续扩展 S025-S028 同题方法竞争图谱。
