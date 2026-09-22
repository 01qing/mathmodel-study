# Architecture Boundary

## 原版是正式生产链
`paper-workflow-orchestrator` 管理 S0-S8，并以当前文件与哈希为权威。

## 本 Skill 是教学旁路
读取原版 contract，增加解释、比较、论文精读、训练、复盘、知识沉淀。

## 禁止双真相源
- 原题解析：优先 `problem_analysis.json`
- 正式模型路线：优先 `model_route.json`
- 正式运行事实：优先 `run_manifest.json` + result contracts
- 正式证据状态：优先 `evidence_gate_report.json`

学习层可以质疑正式路线，但应写成“学习分析/改进建议”，不能篡改正式状态。

## 目录所有权
学习层拥有：
- `learning_sources/`
- `learning_output/`
- `knowledge_base/`

正式层拥有：
- `problem_files/`
- `crawled_data/`
- `paper_output/`
