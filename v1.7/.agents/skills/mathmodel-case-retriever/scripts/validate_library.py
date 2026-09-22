"""Integrity and retrieval smoke checks; not modeling-quality evaluation."""
import json,hashlib
from pathlib import Path
from collections import Counter
from search_cases import search,A

def run():
    papers=json.loads((A/'papers.json').read_text(encoding='utf-8'));byid={p['paper_id']:p for p in papers}
    split=json.loads((A/'split_manifest.json').read_text(encoding='utf-8'))
    assert len(papers)==len(byid)==45
    assert Counter(p['split'] for p in papers)=={'train':32,'dev':7,'test':6}
    expected=hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest()
    assert expected in (A/'split_manifest.sha256').read_text()
    groups={}
    for p in papers:
        assert p['case_group'] not in groups or groups[p['case_group']]==p['split']
        groups[p['case_group']]=p['split']
    pages={i:{p['page']:p['text'] for p in json.loads((A/byid[i]['text_pages_file']).read_text(encoding='utf-8'))} for i in byid}
    chunks=json.loads((A/'chunks.json').read_text(encoding='utf-8'))
    for c in chunks:
        p=byid[c['paper_id']];assert c['split']==p['split'] and c['case_group']==p['case_group']
        raw=pages[c['paper_id']][c['page']]
        assert raw[c['start_char']:c['start_char']+len(c['text'])]==c['text']
    for p in papers:
        assert set(p['reviewed_pages'])<=set(pages[p['paper_id']])
    for args in [('',),('abc','bad'),('abc','evaluation',0)]:
        try:search(*args)
        except ValueError:pass
        else:raise AssertionError('Invalid input accepted')
    result=search('总功率约束下实时分配各台风机功率以降低累计疲劳损伤',top=3)
    assert set(result['candidate_pool_groups'])==set(split['train_groups'])
    assert result['matches'] and any(m['case_group']=='2024-A' for m in result['matches'])
    for m in result['matches']:
        assert byid[m['paper_id']]['split']=='train'
        assert m['excerpt'] in pages[m['paper_id']][m['page']]
    return {'status':'PASS','papers':45,'chunks_verified':len(chunks),'split_counts':dict(Counter(p['split'] for p in papers)), 'checks':['group isolation','frozen split hash','all chunk/page roundtrips','review page bounds','invalid input rejection','train-only retrieval smoke'], 'quality_evaluation':'NOT_RUN; no gold labels or unseen-problem modeling evaluation', 'smoke_matches':[{k:m[k] for k in ['paper_id','case_group','page']} for m in result['matches']]}
if __name__=='__main__':
    result=run();out=A.parents[3]/'learning_output/retriever-validation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
