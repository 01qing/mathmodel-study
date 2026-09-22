# VALIDATION v1.23

- S019 full-text review: PASS (60/60 indexed text pages)
- S019 appendix evidence: PASS as file-manifest audit only; author source bodies NOT AVAILABLE in current worktree
- S019 figure/table argumentation index: PASS (52 figures, 11 tables)
- v1.23 regression: 64/64 PASS
- v1.23 S019 retrieval regression: PASS
- v1.9 G老师/G老师2 code-link regression: PASS
- learning workspace validation: PASS
- paper metadata count: 45
- retrieval chunk count: 6752
- split counts: train=32, dev=7, test=6
- reviewed train: S001-S012, S017-S019
- reviewed dev: none
- reviewed test: none
- S020: train and still unread
- split_manifest SHA256: 0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347

## Historical-test maintenance
Two older tests encoded transient workflow state (S019 must remain pending/unread). Those assertions were changed to durable invariants: S017/S018 assets must remain reviewed and S020/dev/test must remain protected. No learned S017/S018 knowledge was removed.

## Environment limitation
The original 45 PDFs are referenced by Windows `D:\...` paths and cannot all be reopened from the current Linux container. This validation therefore certifies the current indexed assets, rules, retrieval behavior and frozen split; it is not a fresh physical-PDF hash pass.
