# Evidence And Verification

统一状态：

- `author_claim`: 作者明确声称，未独立核验
- `verified`: 已通过原始证据、公式检查、数据核对或代码复现确认
- `partially_verified`: 只核验部分环节
- `not_verified`: 当前无充分核验
- `contradicted`: 发现证据冲突
- `our_inference`: 我们自己的判断

## 严格规则

1. 未运行代码，不得写“复现成功”。
2. 图表存在不等于计算正确。
3. 作者给出评价指标，不等于划分方式合理。
4. 获奖等级若只来自 README/作者自述，应保留 `award_verified=false`。
5. 学术文献支持“方法一般性质”，不能自动证明“该题中效果最佳”。
