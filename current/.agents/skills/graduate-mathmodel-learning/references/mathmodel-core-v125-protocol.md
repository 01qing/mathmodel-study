# MathModel-Core v1.25+ 训练协议

从 v1.25 / S025 起生效。当前共享 Skill 的产品定位为 **MathModel-Core**；兼容目录名仍为 `graduate-mathmodel-learning`。当前不得创建或复制 Master / Architect / Engineer / Writer / Reviewer 角色 Skill。

每篇 train 论文的主节奏：

1. 全文学习
2. 代码 / 公式 / 图表审计
3. Candidate Model Competition
4. 6 小时 Baseline
5. 可迁移方法模块
6. 错误模式
7. Reproduction Level R0-R7
8. 更新同题 Same-Problem Method Competition Map
9. 更新 Skill 规则
10. 专项 + 历史回归

完整 case group 结束后执行 Mini Transfer Test；未到题组末尾不得为了测试而提前打开 test 论文，Dev 也只在需要规则调优时使用。

关键结构文件：
- `knowledge_base/core_schema/mathmodel_core_question_schema_v1.json`
- `knowledge_base/core_schema/reproduction_levels_v1.json`
- `knowledge_base/core_schema/result_registry_schema_v1.json`
- `knowledge_base/core_schema/method_composer_contract_v1.json`
- `knowledge_base/core_schema/figure_decision_rule_schema_v1.json`

旧 S001-S020 不无差别重读。迁移脚本默认只输出缺口，不改写旧卡。
