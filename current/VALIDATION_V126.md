# VALIDATION V1.26

## 结论

**PASS WITH HISTORICAL-RETRIEVAL EXECUTION NOTE** — S026 新资产、规则回归、库完整性和 2025-A 新检索均通过；v1.26 可封存为下一稳定增量。

## v1.26 新增专项

- `test_v126_regressions.py`：**68/68 PASS**。
- `test_v126_2025A_retrieval.py`：**PASS**。
- S026 Result Registry validator：**PASS / 12 checks / 0 arithmetic issues**。
- S025↔S026 Method Composer contract：`compatible_after_adapter`，且明确阻断 fake-QPSO label 与未实现 DPEA mainline。

## 历史规则兼容

以下历史规则脚本在 v1.26 工作树逐项重跑并全部 PASS：

`v1.6, v1.8 code learning, v1.9, v1.10, v1.11, v1.12, v1.13, v1.14, v1.15, v1.16, v1.17, v1.18, v1.19, v1.20, v1.21, v1.22, v1.23, v1.24, v1.25, v1.26`。

2025-E code-link regression：PASS。

## 历史检索执行说明

- v1.26 新增 S026 retrieval：PASS。
- 2024-A 两项历史 retrieval 在本版本实际重跑：PASS。
- 尝试整批重跑全部旧 retrieval 时，纯 Python 检索批处理超过当前单次执行时间上限；这不是断言失败。
- `search_cases.py` SHA256 与 v1.25 **完全相同**。
- `chunks.json` SHA256 与 v1.25 **完全相同**。
- v1.25 已完整验证 2024-A/B/C/E 历史 retrieval；v1.26 没修改检索引擎和 chunk corpus，只新增 S026 MathModel-Core summary/metadata。

因此本版本不把“整批历史检索超时”伪报为 PASS，但已有证据支持旧检索逻辑未发生实现级退化。

## Library / split

`validate_library.py`：**PASS**。

- papers = 45
- chunks_verified = 6752
- split = 32 / 7 / 6
- group isolation = PASS
- frozen split hash = PASS
- all chunk/page roundtrips = PASS
- review page bounds = PASS
- invalid input rejection = PASS
- train-only retrieval smoke = PASS

边界：S027/S028 train 仍未读；S029/S030 dev 未读；所有 test 未读。

## 复现声明

S026 = **R2**。98页全文、原 PDF 全页视觉扫描、打印 MATLAB Appendix 静态审计完成。无作者原始 `.m` + 完整输入 bundle + MATLAB运行，且 Q3 DPEA 实现未见，所以不得声明 R3/R4/R5/R6/R7。

## Mini Transfer Test

NOT_DUE。2025-A case group 尚缺 S027、S028。
