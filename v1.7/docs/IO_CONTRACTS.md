# 学习扩展 I/O Contract 规范

## 1. 通用字段

所有本扩展生成的 JSON 建议包含：

```json
{
  "schema_version": "0.3",
  "record_id": "...",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "producer": "graduate-mathmodel-learning"
}
```

## 2. 可追溯性

引用外部资料时，至少保存：
- `source_id`
- `path_or_url`
- `source_type`
- `competition_year`
- `problem_id`
- `sha256`（本地文件可计算时）
- `retrieved_at`
- `verification_status`

## 3. 验证状态

统一枚举：

- `author_claim`：论文作者明确声称，但我们未独立核验
- `verified`：关键证据或代码已经独立核验
- `partially_verified`：只验证了部分
- `not_verified`：目前未验证
- `contradicted`：发现证据与主张矛盾
- `our_inference`：我们的分析，不是原作者陈述

禁止把 `author_claim` 写成 `verified`。

## 4. 学习掌握等级

统一枚举：

- `unseen`
- `introduced`
- `can_explain`
- `can_apply_with_help`
- `can_apply_independently`
- `can_compare_and_adapt`

升级要求：
- `can_explain`：能解释核心思想和适用条件
- `can_apply_with_help`：能在提示下完成建模
- `can_apply_independently`：至少有一次独立训练或真实做题证据
- `can_compare_and_adapt`：能比较替代模型并说明切换条件

## 5. 正式证据隔离

以下文件仅可读取，不由学习扩展伪造：
- `paper_output/results/run_manifest.json`
- `paper_output/qa/evidence_gate_report.json`
- `paper_output/format_check_report.json`

若学习复现另起实验，输出到：
`learning_output/analyses/...`
或使用正式 S4-S6 完整运行后再引用正式 contract。

## 6. 失效规则

若某知识卡依赖的源文件 hash 改变：
- 卡片不必删除
- 其 `verification_status` 应降为 `not_verified` 或标记 stale
- 需要重新核验后恢复

若正式 `model_route.json` 改变：
- 相关 session 中的“与正式路线比较”部分应标记 stale
- 不应修改历史原始 session 内容，可新增 revision
