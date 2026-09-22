# VALIDATION v1.22

- S018 full-text review: PASS (81/81 indexed text pages)
- S018 printed appendix static audit: PASS as static evidence only; end-to-end author reproduction NOT RUN
- S018 figure/table argumentation index: PASS (53 figures, 10 tables)
- S018 contract replay: PASS as audit; identified expected paper/code/numeric inconsistencies
- v1.22 regressions: 73/73 PASS
- v1.22 S018 retrieval regression: PASS
- historical rule regressions v1.6-v1.22: PASS
- historical retrieval regressions 2024-A/B/C + 2024-E S017 + v1.9 code links: PASS
- paper metadata count: 45
- retrieval chunk count: 6752
- split counts: train=32, dev=7, test=6
- reviewed train papers: S001-S012, S017, S018
- reviewed dev papers: none
- reviewed test papers: none
- split_manifest SHA256: 0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347

## Important limitation
The current container cannot re-open the 45 original PDFs through the Windows D:\ paths stored in `local_papers_2024_2025.json`. Therefore original-file byte/page/hash validation was not rerun in this environment. This validation certifies the present Skill assets, regression behavior, indexed metadata and frozen split state, not a fresh physical-PDF identity pass.
