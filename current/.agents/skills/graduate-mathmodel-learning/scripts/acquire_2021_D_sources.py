#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, os, sys, urllib.parse, urllib.request

p=argparse.ArgumentParser()
p.add_argument("--manifest", default=".agents/skills/graduate-mathmodel-learning/assets/cases/2021_D_source_acquisition_manifest.json")
p.add_argument("--output-root", default="learning_sources/competitions/2021/D")
p.add_argument("--source", choices=["xlsx","csv","both"], default="both")
p.add_argument("--verify-only", action="store_true")
p.add_argument("--timeout", type=int, default=60)
args=p.parse_args()

manifest=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
root=Path(args.output_root)
root.mkdir(parents=True,exist_ok=True)

def git_blob_sha1(data):
    header=f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header+data).hexdigest()

def raw_url(repo,ref,path):
    owner,name=repo.split("/",1)
    enc=urllib.parse.quote(path, safe="/")
    return f"https://raw.githubusercontent.com/{owner}/{name}/{ref}/{enc}"

def verify(path,meta):
    if not path.exists():
        return {"status":"MISSING","path":str(path)}
    data=path.read_bytes()
    size=len(data)
    sha=git_blob_sha1(data)
    return {
        "status":"PASS" if size==meta["size"] and sha==meta["git_blob_sha1"] else "HASH_MISMATCH",
        "path":str(path),
        "size":size,
        "expected_size":meta["size"],
        "git_blob_sha1":sha,
        "expected_git_blob_sha1":meta["git_blob_sha1"]
    }

def acquire_one(repo,ref,meta,dest):
    current=verify(dest,meta)
    if current["status"]=="PASS":
        current["action"]="reused_verified_file"
        return current
    if args.verify_only:
        current["action"]="verify_only"
        return current
    url=raw_url(repo,ref,meta["path"])
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"graduate-mathmodel-learning-skill/1.2"})
        with urllib.request.urlopen(req,timeout=args.timeout) as resp:
            data=resp.read()
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data)
        result=verify(dest,meta)
        result["action"]="downloaded"
        result["url"]=url
        if result["status"]!="PASS":
            dest.unlink(missing_ok=True)
        return result
    except Exception as e:
        return {
            "status":"NETWORK_BLOCKED",
            "path":str(dest),
            "url":url,
            "error":f"{type(e).__name__}: {e}",
            "action":"download_failed"
        }

items=[]

if args.source in {"xlsx","both"}:
    block=manifest["primary_xlsx_mirror"]
    for meta in block["files"]:
        dest=root/"xlsx"/meta["name"]
        r=acquire_one(block["repository"],block["ref"],meta,dest)
        r.update({"source_role":block["source_role"],"repository":block["repository"],"repo_path":meta["path"]})
        items.append(r)

if args.source in {"csv","both"}:
    block=manifest["participant_csv_mirror"]
    for split in ["train","test"]:
        for meta in block[split]:
            dest=root/"csv_mirror"/split/meta["name"]
            r=acquire_one(block["repository"],block["ref"],meta,dest)
            r.update({"source_role":block["source_role"],"repository":block["repository"],"repo_path":meta["path"],"split":split})
            items.append(r)

statuses=[x["status"] for x in items]
if items and all(s=="PASS" for s in statuses):
    overall="READY_FOR_AUDIT"
elif "HASH_MISMATCH" in statuses:
    overall="HASH_MISMATCH"
elif "NETWORK_BLOCKED" in statuses:
    overall="NETWORK_BLOCKED"
elif "MISSING" in statuses:
    overall="MISSING"
else:
    overall="PARTIAL"

report={
    "schema_version":"1.2",
    "case_id":"gmcm-2021-D",
    "overall_status":overall,
    "source_request":args.source,
    "verify_only":args.verify_only,
    "items":items,
    "meaning":{
        "READY_FOR_AUDIT":"All requested files are materialized and match manifest Git blob SHA/size. Data contents are not yet audited.",
        "NETWORK_BLOCKED":"At least one requested source could not be reached.",
        "HASH_MISMATCH":"At least one local/downloaded file differs from the recorded Git blob.",
        "MISSING":"At least one required local file is missing in verify-only mode."
    }
}
out=root/"source_acquisition_report.json"
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"[{overall}] {out}")
if overall not in {"READY_FOR_AUDIT"}:
    sys.exit(2)
