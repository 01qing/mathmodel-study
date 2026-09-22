"""Page-cited candidate retrieval. Rank scores do not establish transferability."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

A=Path(__file__).resolve().parents[1]/'assets'
def search(query,mode='evaluation',top=6):
    if not query.strip():raise ValueError('Query required')
    if not isinstance(top,int) or isinstance(top,bool) or not 1<=top<=20:raise ValueError('top must be 1..20')
    if mode not in ['evaluation','production']:raise ValueError('Unknown mode')
    allchunks=json.loads((A/'chunks.json').read_text(encoding='utf-8'))
    chunks=[x for x in allchunks if mode=='production' or x['split']=='train']
    papers={p['paper_id']:p for p in json.loads((A/'papers.json').read_text(encoding='utf-8'))}
    vectorizer=TfidfVectorizer(analyzer='char',ngram_range=(2,4),max_features=60000,sublinear_tf=True)
    X=vectorizer.fit_transform(c['text'] for c in chunks);q=vectorizer.transform([query]);scores=(X@q.T).toarray().ravel()
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
             'transferability':'REQUIRES_READING_AND_STRUCTURAL_REVIEW'})
        if len(chosen)>=top:break
    return {'mode':mode,'query':query,'candidate_pool_groups':sorted(set(c['case_group'] for c in chunks)),
      'split_manifest_sha256':hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest(),
      'query_keyword_tags':qt,'matches':chosen,'scope':'Heuristic candidate retrieval; automatic tags do not resolve negation, causality or assumptions'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--query',required=True);p.add_argument('--mode',choices=['evaluation','production'],default='evaluation');p.add_argument('--top',type=int,default=6);p.add_argument('--output',type=Path)
    args=p.parse_args()
    if not 1<=args.top<=20:p.error('top must be 1..20')
    result=search(args.query,args.mode,args.top);text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text,encoding='utf-8')
    else:print(text)
