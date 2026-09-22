#!/usr/bin/env python3
"""Static audit of a modeling code bundle. It finds evidence and risks; it does not execute models."""
from __future__ import annotations
import argparse, ast, hashlib, json, re
from collections import Counter
from pathlib import Path

DATA_EXTS = ("csv","xlsx","xls","mat","npy","npz","json","yaml","yml","pth","pt","joblib","pkl")
DATA_RE = re.compile(r"[\"']([^\"'\n]+\.(?:" + "|".join(DATA_EXTS) + r"))[\"']", re.I)
WIN_ABS_RE = re.compile(r"[A-Za-z]:[\\/][^\"'\n]+")
POSIX_ABS_RE = re.compile(r"(?<![A-Za-z0-9_])/(?:home|mnt|data|tmp|Users|opt|var)/[^\"'\n]+")
PLOT_TOKENS = ("matplotlib", "plt.", "seaborn", "sns.", "savefig", "scatter(", "bar(", "plot(", "heatmap(", "boxplot(", "violin")
SPLIT_TOKENS = ("train_test_split", "StratifiedKFold", "StratifiedGroupKFold", "GroupKFold", "KFold", "random.shuffle", "split")
ADAPT_TOKENS = ("coral", "mmd", "domain", "entropy_minimization", "transfer", "adapt")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def decode_text(p: Path):
    raw = p.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "gb18030", "latin1"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            pass
    return None, None


def py_info(p: Path, text: str):
    out = {"syntax": "PASS", "imports": [], "functions": [], "classes": [], "cli_args": []}
    try:
        tree = ast.parse(text, filename=str(p))
    except SyntaxError as e:
        out.update({"syntax": "FAIL", "syntax_error": f"{e.msg} line {e.lineno}"})
        return out
    imports, funcs, classes, cli = set(), [], [], []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imports.update(a.name for a in n.names)
        elif isinstance(n, ast.ImportFrom):
            imports.add(n.module or "")
        elif isinstance(n, ast.FunctionDef):
            funcs.append(n.name)
        elif isinstance(n, ast.ClassDef):
            classes.append(n.name)
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "add_argument":
            for a in n.args[:1]:
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    cli.append(a.value)
    out.update({"imports": sorted(imports), "functions": funcs, "classes": classes, "cli_args": cli})
    return out


def audit(root: Path):
    files = [p for p in root.rglob("*") if p.is_file()]
    report = {
        "schema_version": "0.1",
        "scope": "STATIC_CODE_BUNDLE_AUDIT_NOT_MODEL_REPRODUCTION",
        "root": str(root),
        "file_count": len(files),
        "extensions": dict(Counter((p.suffix.lower() or "<none>") for p in files)),
        "python": [],
        "textual_files": [],
        "data_references": [],
        "hardcoded_absolute_paths": [],
        "plotting_files": [],
        "split_related_files": [],
        "domain_adaptation_related_files": [],
        "limitations": [
            "Static inspection does not prove numerical correctness or end-to-end runnability",
            "Referenced datasets/weights may be absent from the bundle",
            "Text pattern matches require manual interpretation"
        ]
    }
    data_refs, abs_paths = set(), set()
    for p in files:
        rel = str(p.relative_to(root))
        if p.suffix.lower() in {".py", ".m", ".yaml", ".yml", ".txt", ".md", ".json"}:
            text, enc = decode_text(p)
            if text is None:
                continue
            entry = {"path": rel, "sha256": sha256(p), "encoding": enc, "lines": len(text.splitlines())}
            report["textual_files"].append(entry)
            if p.suffix.lower() == ".py":
                q = dict(entry); q.update(py_info(p, text)); report["python"].append(q)
            for x in DATA_RE.findall(text): data_refs.add(x)
            for x in WIN_ABS_RE.findall(text): abs_paths.add(x)
            for x in POSIX_ABS_RE.findall(text): abs_paths.add(x)
            low = text.lower()
            if any(t.lower() in low for t in PLOT_TOKENS): report["plotting_files"].append(rel)
            if any(t.lower() in low for t in SPLIT_TOKENS): report["split_related_files"].append(rel)
            if any(t.lower() in low for t in ADAPT_TOKENS): report["domain_adaptation_related_files"].append(rel)
    report["data_references"] = sorted(data_refs)
    report["hardcoded_absolute_paths"] = sorted(abs_paths)
    for k in ("plotting_files", "split_related_files", "domain_adaptation_related_files"):
        report[k] = sorted(set(report[k]))
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    if not a.root.is_dir(): raise SystemExit(f"not a directory: {a.root}")
    r = audit(a.root)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    bad = [x for x in r["python"] if x.get("syntax") != "PASS"]
    print(json.dumps({"files": r["file_count"], "python": len(r["python"]), "python_syntax_fail": len(bad), "absolute_paths": len(r["hardcoded_absolute_paths"]), "data_refs": len(r["data_references"]), "plotting_files": len(r["plotting_files"])}, ensure_ascii=False))

if __name__ == "__main__":
    main()
