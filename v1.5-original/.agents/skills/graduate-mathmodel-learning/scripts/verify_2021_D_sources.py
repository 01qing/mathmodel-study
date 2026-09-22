#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, sys

p=argparse.ArgumentParser()
p.add_argument("--manifest", default=".agents/skills/graduate-mathmodel-learning/assets/cases/2021_D_source_acquisition_manifest.json")
p.add_argument("--root", default="learning_sources/competitions/2021/D")
args=p.parse_args()

manifest=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
root=Path(args.root)

def blob_sha(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()

rows=[]
def check(meta,path,role):
    if not path.exists():
        return {"name":meta["name"],"role":role,"status":"MISSING","path":str(path)}
    b=path.read_bytes()
    sha=blob_sha(b)
    return {
        "name":meta["name"],"role":role,"path":str(path),
        "status":"PASS" if len(b)==meta["size"] and sha==meta["git_blob_sha1"] else "HASH_MISMATCH",
        "size":len(b),"expected_size":meta["size"],
        "git_blob_sha1":sha,"expected_git_blob_sha1":meta["git_blob_sha1"]
    }

x=manifest["primary_xlsx_mirror"]
for meta in x["files"]:
    rows.append(check(meta,root/"xlsx"/meta["name"],"contest_attachment_mirror"))
c=manifest["participant_csv_mirror"]
for split in ["train","test"]:
    for meta in c[split]:
        rows.append(check(meta,root/"csv_mirror"/split/meta["name"],f"participant_csv_{split}"))

out={"schema_version":"1.2","case_id":"gmcm-2021-D","files":rows}
out["status"]="PASS" if all(r["status"]=="PASS" for r in rows) else "FAIL"
(root/"source_verification.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"[{out['status']}] verified {sum(r['status']=='PASS' for r in rows)}/{len(rows)} files")
sys.exit(0 if out["status"]=="PASS" else 1)
