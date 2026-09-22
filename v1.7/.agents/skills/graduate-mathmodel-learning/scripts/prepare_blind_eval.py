#!/usr/bin/env python3
from pathlib import Path
import json, shutil, argparse

p = argparse.ArgumentParser()
p.add_argument("--case-id", default="gmcm-2021-D")
p.add_argument("--output", default="learning_output/blind_eval/gmcm-2021-D")
args = p.parse_args()

ROOT = Path.cwd()
SKILL = ROOT/".agents"/"skills"/"graduate-mathmodel-learning"
out = ROOT/args.output
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True, exist_ok=True)

facts = SKILL/"assets"/"cases"/"2021_D_problem_facts.json"
rubric = SKILL/"assets"/"cases"/"2021_D_blind_eval_rubric.json"
template = SKILL/"templates"/"blind_answer.json"

for src,name in [
    (facts,"problem_facts.json"),
    (rubric,"rubric.json"),
    (template,"answer_template.json")
]:
    shutil.copy2(src,out/name)

instructions = """# Fresh Blind Eval: gmcm-2021-D

## Allowed inputs
- 本目录 `problem_facts.json`
- 实际题面
- 4个原始附件
- graduate-mathmodel-learning 的通用规则

## Forbidden inputs
- 优秀论文 PDF
- paper-screening-2021-D.md
- reference-baseline-2021-D.md
- 2021_D_case_manifest.json 中的 paper_screening 字段
- 任何论文专属模型、结果或特征名单

## Task
对 Q1-Q4 分别输出：
1. 问题抽象
2. 至少3条候选路线
3. 推荐路线
4. 为什么不选其它路线
5. 验证方案
6. 风险
7. 切换条件

保存为 `answer.json`，并设置：
`contamination_status = fresh_blind`

## Attachments
如果项目里已有：
`learning_sources/competitions/2021/D/problem/`
`learning_sources/competitions/2021/D/data/`

可复制/只读使用。

不要复制：
`papers/`
`expert_commentary/`
"""

(out/"EVAL_INSTRUCTIONS.md").write_text(instructions,encoding="utf-8")

# Copy only problem/data attachments when present.
case_dir = ROOT/"learning_sources"/"competitions"/"2021"/"D"
for sub in ["problem","data"]:
    src = case_dir/sub
    if src.exists():
        dst = out/"attachments"/sub
        shutil.copytree(src,dst)

guard = {
    "case_id":"gmcm-2021-D",
    "forbidden_tokens":[
        "D21102700119","D21104860088",
        "paper-screening-2021-D",
        "reference-baseline-2021-D"
    ],
    "forbidden_directories":["papers","expert_commentary"],
    "status":"BLIND_BUNDLE_PREPARED"
}
(out/"contamination_guard.json").write_text(
    json.dumps(guard,ensure_ascii=False,indent=2),encoding="utf-8"
)
print("[PASS] blind bundle prepared:", out)
