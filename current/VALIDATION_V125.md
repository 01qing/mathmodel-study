# VALIDATION V1.25

## 结果

**PASS** — v1.25 可以作为 MathModel-Core 新协议的首个稳定基线版本。

## 新增专项验证

- `test_v125_regressions.py`：PASS。
- `test_v125_2025A_retrieval.py`：PASS。
- Result Registry validator：PASS，并正确抓到 S025 Conv_Case0 transfer improvement 符号漂移。
- Method Composer 七门合同：PASS（S025 推荐组合需 shared schema adapter）。
- legacy schema coverage：PASS；旧卡只报告缺口，不自动重读/改写。

## 历史兼容

- graduate-mathmodel-learning 历史规则回归：v1.6、v1.8、v1.9、v1.10-v1.24 以及 v1.25 全部逐项 PASS。
- 历史检索：2024-A、2024-B、2024-C、2024-E 全部逐项 PASS。
- 2025-E code-link regression：PASS。
- 2025-A S025 Core retrieval：PASS。

## 库完整性

`validate_library.py`：PASS。

- papers = 45
- chunks_verified = 6752
- split = 32 / 7 / 6
- reviewed dev = []
- reviewed test = []
- frozen split SHA256 = `0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`

## 复现声明边界

S025 = **R2**。全文、原 PDF 视觉和打印代码静态审计已完成；未获得作者原始可执行源码 + 完整输入数据，因此不得宣称 API 烟测、真实数据复现、端到端复现或独立重实现成功。

## Mini Transfer Test

NOT_DUE。必须等 S025-S028 训练论文闭环后再执行，当前不以“协议升级”为理由打开 test。
