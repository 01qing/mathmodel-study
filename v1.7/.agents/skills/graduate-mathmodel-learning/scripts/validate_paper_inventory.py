"""Verify local PDF identities and declared review coverage, not the truth of reviews."""
import argparse,hashlib,json
from pathlib import Path

def validate(papers,base):
    errors=[]; seen=set()
    for p in papers:
        try:
            sid=p['source_id']
            if sid in seen: errors.append('duplicate source: '+sid)
            seen.add(sid)
            path=Path(p['path']); path=path if path.is_absolute() else base/path
            if not path.is_file(): raise ValueError('missing PDF: '+str(path))
            data=path.read_bytes()
            if not data.startswith(b'%PDF-'): raise ValueError('not a PDF: '+str(path))
            if hashlib.sha256(data).hexdigest()!=p['sha256']: raise ValueError('hash mismatch: '+sid)
            count=p['page_count']; pages=p.get('reviewed_pages',[])
            if type(count) is not int or count<1: raise ValueError('invalid page count')
            import pymupdf
            with pymupdf.open(path) as doc:
                if len(doc)!=count: raise ValueError('actual PDF page count differs: '+sid)
            if any(type(n) is not int or not 1<=n<=count for n in pages) or len(pages)!=len(set(pages)):
                raise ValueError('invalid reviewed pages: '+sid)
            if p['review_status'] not in ['not_reviewed','partial','full']: raise ValueError('invalid review status')
            if p['review_status']=='full' and set(pages)!=set(range(1,count+1)): raise ValueError('full review lacks coverage: '+sid)
            if p['review_status']=='partial' and not pages: raise ValueError('partial review lacks pages: '+sid)
            if p['review_status']=='not_reviewed' and pages: raise ValueError('inconsistent review state: '+sid)
            if pages and not p.get('review_evidence'): raise ValueError('review notes missing: '+sid)
        except Exception as e: errors.append(str(e))
    return errors

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--manifest',type=Path,required=True);args=a.parse_args()
    d=json.loads(args.manifest.read_text(encoding='utf-8'));errors=validate(d['papers'],args.manifest.parent)
    if d.get('materialized_count')!=len(d['papers']):errors.append('materialized count mismatch')
    print(json.dumps({'status':'FAIL' if errors else 'FILE_IDENTITIES_AND_DECLARED_COVERAGE_PASS','errors':errors,
                      'scope':'Checks PDF page counts and declared coverage; does not certify full reading or scientific correctness'},ensure_ascii=False,indent=2))
    raise SystemExit(bool(errors))
