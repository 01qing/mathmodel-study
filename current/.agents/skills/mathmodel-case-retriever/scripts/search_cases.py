"""Page-cited candidate retrieval. Rank scores do not establish transferability."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

A=Path(__file__).resolve().parents[1]/'assets'

def _load_code_links():
    path=A/'code_case_links.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

def _links_for_case_group(case_group):
    return _load_code_links().get(case_group,[])

def _load_core_summaries():
    path=A/'core_retrieval_summaries.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

def _core_summary(paper_id):
    return _load_core_summaries().get(paper_id)

def _load_case_group_maps():
    path=A/'case_group_maps.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

def _case_group_map(case_group):
    return _load_case_group_maps().get(case_group)

_INDEX_CACHE=None

def _reviewed_train_index():
    # Process-local cache only: identical corpus/vectorizer semantics, but repeated
    # evaluation/production calls in one validation run do not rebuild TF-IDF.
    global _INDEX_CACHE
    chunks_path=A/'chunks.json'; papers_path=A/'papers.json'
    stamp=(chunks_path.stat().st_mtime_ns,papers_path.stat().st_mtime_ns)
    if _INDEX_CACHE is not None and _INDEX_CACHE[0]==stamp:
        return _INDEX_CACHE[1:]
    allchunks=json.loads(chunks_path.read_text(encoding='utf-8'))
    papers={p['paper_id']:p for p in json.loads(papers_path.read_text(encoding='utf-8'))}
    reviewed={pid:set(p.get('reviewed_pages',[])) for pid,p in papers.items()}
    chunks=[x for x in allchunks if x['split']=='train' and x['page'] in reviewed[x['paper_id']]]
    vectorizer=TfidfVectorizer(analyzer='char',ngram_range=(2,4),max_features=60000,sublinear_tf=True)
    X=vectorizer.fit_transform(c['text'] for c in chunks)
    _INDEX_CACHE=(stamp,chunks,papers,vectorizer,X)
    return chunks,papers,vectorizer,X

def search(query,mode='evaluation',top=6):
    if not query.strip():raise ValueError('Query required')
    if not isinstance(top,int) or isinstance(top,bool) or not 1<=top<=20:raise ValueError('top must be 1..20')
    if mode not in ['evaluation','production']:raise ValueError('Unknown mode')
    chunks,papers,vectorizer,X=_reviewed_train_index()
    q=vectorizer.transform([query]);scores=(X@q.T).toarray().ravel()
    ontology=json.loads((A/'ontology.json').read_text(encoding='utf-8'))
    qt={kind:[tag for tag,words in tags.items() if any(w.lower() in query.lower() for w in words if len(w)>1)] for kind,tags in ontology.items()}
    # Lexical shortlist limits spurious matches from broad automatically extracted tags.
    short=np.argsort(-scores)[:80]
    def rank(i):
        c=chunks[i];matches=sum(len(set(qt[k])&set(c['tags'][k])) for k in qt)
        return (float(scores[i]),matches)
    ranked=sorted(short,key=rank,reverse=True);chosen=[];seen=set()
    for i in ranked:
        if scores[i]<=0:continue
        c=chunks[i]
        if c['paper_id'] in seen:continue
        p=papers[c['paper_id']];seen.add(c['paper_id'])
        chosen.append({'paper_id':p['paper_id'],'case_group':p['case_group'],'title':p.get('paper_title',p['title']),'page':c['page'],
             'reading_status':p['learning_status'],'review_file':p.get('review_file'),
             'source_path':p['source_path'],'source_sha256':p['sha256'],'chunk_id':c['chunk_id'],'excerpt':c['text'],
             'lexical_cosine':float(scores[i]),'matched_keyword_tags':{k:sorted(set(qt[k])&set(c['tags'][k])) for k in qt},
             'transferability':'REQUIRES_READING_AND_STRUCTURAL_REVIEW',
             'supplemental_code_cases':_links_for_case_group(p['case_group']),
             'same_problem_cross_paper_map':_case_group_map(p['case_group']),
             'mathmodel_core_summary':_core_summary(p['paper_id'])})
        if len(chosen)>=top:break
    return {'mode':mode,'query':query,'candidate_pool_groups':sorted(set(c['case_group'] for c in chunks)),
      'split_manifest_sha256':hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest(),
      'query_keyword_tags':qt,'matches':chosen,
      'supplemental_code_boundary':'Supplemental code links are method-level learning aids, not proof that the code belongs to the matched paper.',
      'scope':'Heuristic candidate retrieval; automatic tags do not resolve negation, causality or assumptions'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--query',required=True);p.add_argument('--mode',choices=['evaluation','production'],default='evaluation');p.add_argument('--top',type=int,default=6);p.add_argument('--output',type=Path)
    args=p.parse_args()
    if not 1<=args.top<=20:p.error('top must be 1..20')
    result=search(args.query,args.mode,args.top);text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text,encoding='utf-8')
    else:print(text)
