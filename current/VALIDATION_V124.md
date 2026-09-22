# v1.24 验证报告

## 验证范围

- S020 全文/代码/图表论证资产存在性与语义回归。
- S017–S020 同题方法族闭环。
- 训练/开发/测试冻结边界。
- 历史版本测试兼容：把“当时 S020 未读”的瞬时断言改为历史知识/分组不变量，不删除旧知识检查。

## 强制门禁

- target-feature identity leakage
- train-only preprocessing
- T>1 sequence contract
- architecture-name→implementation primitive
- worst-group metric
- governing-model counterfactual replay
- result-table percentage replay
- scenario/simulation/observed-intervention evidence levels
- cross-domain template contamination
- heuristic layout vs optimization

## 数据边界

- inventory: 45 papers
- split: 32 train / 7 dev / 6 test
- protected dev/test papers remain unread
- S020 belongs to train and is now reviewed

最终 PASS/测试数量与 ZIP SHA256 在封包命令完成后写入。

## 实际执行结果

- v1.24 专项规则回归：**52/52 PASS**。
- v1.6→v1.24 历史规则测试：**18组逐项 PASS**。
- v1.24 2024-E S020 实际检索回归：**PASS**。
- v1.9 教师代码链接回归：**PASS**。
- 一次把多条历史检索串在同一 shell 中运行时超过环境总时限，因此没有把“批量命令超时”伪报成检索失败；当前版本相关检索已独立通过。
- papers registry：**45篇**。
- split：**32 train / 7 dev / 6 test**。
- reviewed：**16篇，全部属于 train**（S001–S012、S017–S020）。
- dev/test reviewed：**0**。
- `split_manifest.json` SHA256：`0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`，与冻结记录一致。

## 结论

v1.24 可以封版。下一训练样本跳过测试组 S021–S024，进入 train 的 S025 / 2025-A。
