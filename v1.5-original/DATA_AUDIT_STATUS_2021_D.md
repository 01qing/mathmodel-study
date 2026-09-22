# 2021 D 数据审计状态

当前：`READY_AWAITING_BINARY_FILES`

已确认 GitHub 上四个 Excel 的存在与文件元数据，但当前运行环境尚未取得真实二进制内容。

因此这些真实统计仍为 **NOT_RUN**：
- 五个 ADMET 标签比例
- 729 描述符缺失/常量列
- 三份训练表 SMILES 实际对齐
- IC50/pIC50 逐行误差

文件落到 `learning_sources/competitions/2021/D/data/` 后运行：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/audit_2021_D_data.py \
  --data-dir learning_sources/competitions/2021/D/data
```
