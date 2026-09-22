# First Real Run Checklist

## 2021 D

### A. Materialize actual files
Place under:

```text
learning_sources/competitions/2021/D/data/
```

Required:
- ERα_activity.xlsx
- Molecular_Descriptor.xlsx
- ADMET.xlsx
- 分子描述符含义解释.xlsx

### B. Data audit

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/audit_2021_D_data.py   --data-dir learning_sources/competitions/2021/D/data
```

Require:
`PASS` or understood `PASS_WITH_WARNINGS`.

### C. Fresh blind evaluation
Run in a separate context using the prepared blind bundle.
Do not expose excellent papers.

### D. Standard benchmark

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/benchmark_2021_D_models.py   --data-dir learning_sources/competitions/2021/D/data   --profile standard
```

### E. Final fit

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/finalize_2021_D_models.py   --data-dir learning_sources/competitions/2021/D/data
```

### F. Paper comparison

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/prepare_paper_benchmark_comparison.py
```

Complete Q1-Q4 Agent Review before knowledge extraction.

### G. Knowledge extraction

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/extract_case_knowledge.py
```

### H. Upgrade learning mastery
Only upgrade to `can_apply_independently` if there is independent practice evidence.
