# v1.2 Progress

## 本轮解决的问题

此前已确认远程题目附件和公开 CSV 存在，但“远程存在”与“本地真实审计”之间还缺资料获取和来源等价性门禁。

v1.2 新增：

1. `2021_D_source_acquisition_manifest.json`
2. XLSX 与 CSV 的 repository/path/ref/size/Git blob SHA 元数据
3. `acquire_2021_D_sources.py`
4. `verify_2021_D_sources.py`
5. `audit_2021_D_csv_mirror.py`
6. `crosscheck_2021_D_xlsx_csv.py`
7. Git blob SHA 校验
8. participant CSV 不得自动等价于 contest XLSX 的来源门禁
9. E17-E19 来源治理 eval

## 已确认的远程事实

### XLSX contest-attachment mirror
`zhanwen/MathModel`：
- ADMET.xlsx: 87,227 bytes
- ERα_activity.xlsx: 93,695 bytes
- Molecular_Descriptor.xlsx: 8,804,984 bytes
- 分子描述符含义解释.xlsx: 49,477 bytes

### Participant CSV mirror
`Bureaux-Tao/modeling2021-D`：
train:
- ADMET.csv: 121,691 bytes
- ERα_activity.csv: 125,203 bytes
- Molecular_Descriptor.csv: 6,434,745 bytes

test:
- ADMET.csv: 4,670 bytes
- ERα_activity.csv: 4,510 bytes
- Molecular_Descriptor.csv: 176,346 bytes

真实 ADMET.csv 文本连接已经可以读取；6.4MB descriptor CSV 和 8.8MB XLSX 仍超过当前会话/容器传输能力。

## 当前诚实状态

- Remote metadata：CONFIRMED
- Small CSV text readability：PARTIAL CONFIRMED
- Full XLSX local materialization：NOT_RUN / current runtime network blocked
- Full participant CSV local materialization：NOT_RUN
- XLSX vs CSV cross-check：NOT_RUN
- Real Data Audit：NOT_RUN
- Real Standard Benchmark：NOT_RUN

## 下一跳

在可联网的 Codex/本地环境：

`acquire -> hash verify -> XLSX audit -> CSV audit -> mirror crosscheck -> real benchmark`
