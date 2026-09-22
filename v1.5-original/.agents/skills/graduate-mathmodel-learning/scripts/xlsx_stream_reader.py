#!/usr/bin/env python3
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
import re

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

def col_to_index(ref):
    m = re.match(r"([A-Z]+)", ref or "")
    if not m:
        return 0
    n = 0
    for ch in m.group(1):
        n = n * 26 + ord(ch) - 64
    return n - 1

def shared_strings(zf):
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    out = []
    with zf.open("xl/sharedStrings.xml") as f:
        for event, elem in ET.iterparse(f, events=("end",)):
            if elem.tag == NS + "si":
                out.append("".join((t.text or "") for t in elem.iter(NS+"t")))
                elem.clear()
    return out

def sheet_map(zf):
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {}
    for rel in rels:
        target = rel.attrib.get("Target", "")
        if target.startswith("/"):
            target = target.lstrip("/")
        elif not target.startswith("xl/"):
            target = "xl/" + target
        rel_map[rel.attrib.get("Id")] = target
    out = []
    sheets = wb.find(NS+"sheets")
    for sh in sheets:
        out.append((sh.attrib.get("name",""), rel_map.get(sh.attrib.get(RID))))
    return out

class XlsxBook:
    def __init__(self, path):
        self.path = Path(path)

    def sheet_names(self):
        with zipfile.ZipFile(self.path) as zf:
            return [n for n,_ in sheet_map(zf)]

    def iter_rows(self, sheet_name):
        with zipfile.ZipFile(self.path) as zf:
            shared = shared_strings(zf)
            mapping = dict(sheet_map(zf))
            target = mapping[sheet_name]
            with zf.open(target) as f:
                current = None
                max_idx = -1
                for event, elem in ET.iterparse(f, events=("start","end")):
                    if event == "start" and elem.tag == NS+"row":
                        current = {}
                        max_idx = -1
                    elif event == "end" and elem.tag == NS+"c":
                        if current is None:
                            continue
                        idx = col_to_index(elem.attrib.get("r",""))
                        max_idx = max(max_idx, idx)
                        typ = elem.attrib.get("t")
                        value = None
                        if typ == "inlineStr":
                            value = "".join((t.text or "") for t in elem.iter(NS+"t"))
                        else:
                            v = elem.find(NS+"v")
                            raw = v.text if v is not None else None
                            if raw is None:
                                value = None
                            elif typ == "s":
                                value = shared[int(raw)]
                            elif typ == "b":
                                value = raw == "1"
                            elif typ in ("str","e"):
                                value = raw
                            else:
                                try:
                                    x = float(raw)
                                    value = int(x) if x.is_integer() else x
                                except Exception:
                                    value = raw
                        current[idx] = value
                        elem.clear()
                    elif event == "end" and elem.tag == NS+"row":
                        row = [None]*(max_idx+1) if max_idx >= 0 else []
                        for i,v in (current or {}).items():
                            row[i] = v
                        yield row
                        current = None
                        elem.clear()
