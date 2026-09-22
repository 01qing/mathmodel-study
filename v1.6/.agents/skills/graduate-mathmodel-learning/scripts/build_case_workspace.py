#!/usr/bin/env python3
from pathlib import Path
import argparse, json, shutil

p=argparse.ArgumentParser()
p.add_argument("--manifest", default=".agents/skills/graduate-mathmodel-learning/assets/cases/2021_D_case_manifest.json")
args=p.parse_args()

ROOT=Path.cwd()
manifest_path=ROOT/args.manifest
if not manifest_path.exists():
    raise SystemExit("case manifest not found")

m=json.loads(manifest_path.read_text(encoding="utf-8"))
year=str(m["year"])
pid=m["problem_id"]
base=ROOT/"learning_sources"/"competitions"/year/pid
for sub in ["problem","data","papers","code","expert_commentary","literature","metadata"]:
    (base/sub).mkdir(parents=True,exist_ok=True)

(base/"metadata"/"case_manifest.json").write_text(
    json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8"
)

readme = f"""# {m['case_id']}

Working title: {m['canonical_working_title']}
Title status: {m['title_status']}

## Materialization checklist

- [ ] 题面落盘
- [ ] 所有官方/镜像附件落盘
- [ ] 至少 {m['first_pass_requirements']['minimum_papers_to_download']} 篇优秀论文落盘
- [ ] 优先选择方法不同的论文
- [ ] 论文来源登记
- [ ] 代码如有，单独登记并实际运行后再标记 verified
- [ ] 题名冲突已解决或明确保留 unresolved

不要把这个学习目录中的文件直接当作 paper_output 正式证据。
"""
(base/"README.md").write_text(readme,encoding="utf-8")
print("[PASS] case workspace created:",base)
