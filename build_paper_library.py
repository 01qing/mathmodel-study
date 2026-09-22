"""Build reproducible full-text search assets. Extraction is never marked as learning."""
from pathlib import Path
import json,re,hashlib
from datetime import datetime,timezone
W=Path(__file__).parent;D=W/'v1.7';S=D/'.agents/skills/mathmodel-case-retriever';A=S/'assets';A.mkdir(parents=True,exist_ok=True)
m=json.loads((W/'evidence/manifest.json').read_text(encoding='utf-8'))
dev={'2024-D','2025-B'};test={'2024-F','2025-D'}
papers=[];chunks=[]
ontology={
 'tasks':{'classification':['分类','故障诊断','识别','混淆矩阵'],'regression':['回归','预测','拟合','RMSE'],'optimization':['优化','最小化','最大化','目标函数'],'multiobjective':['多目标','Pareto','帕累托','非支配'],'domain_adaptation':['迁移学习','源域','目标域','域适应'],'factor_analysis':['交互','方差分析','效应量','影响因素'],'segmentation':['分割','像素','二值化'],'geometry':['几何','坐标','曲线','三维重构'],'ranking':['排序','评价指标','熵权','层次分析'],'simulation':['仿真','蒙特卡洛','泊松']},
 'data':{'signal':['波形','频谱','采样率','采样频率','振动信号'],'time_series':['时间序列','时序','实时','时延'],'spatial':['空间','栅格','地理','经纬度'],'image':['图像','视频','像素'],'graph':['图论','拓扑','节点','边','路径'],'tabular':['数据表','描述符','表格','特征变量']},
 'constraints':{'physical':['机理','物理','守恒','量纲'],'resources':['缓存','容量','内存','约束'],'feasibility':['可行域','可行性','边界','约束'],'unlabeled':['无标签','未知标签','未知类别'],'robustness':['鲁棒','噪声','敏感性','灵敏度','不确定性']}}
def tags(text):return {kind:[tag for tag,words in terms.items() if any(w.lower() in text.lower() for w in words)] for kind,terms in ontology.items()}
for x in m:
    if 'pages' not in x or int(x['id'][1:])>45:continue
    path=Path(x['path']);year=2024 if '2024年' in str(path) else 2025;problem=path.parent.name[0];group=f'{year}-{problem}'
    split='dev' if group in dev else 'test' if group in test else 'train'
    raw=Path(x['text_file']).read_text(encoding='utf-8');parts=re.split(r'\n--- PAGE (\d+) ---\n',raw)
    page_records=[]
    for n in range(1,len(parts),2):
        number=int(parts[n]);text=parts[n+1].strip();page_records.append({'page':number,'text':text})
        for start in range(0,len(text),700):
            span=text[start:start+900]
            if len(span.strip())<50:continue
            chunks.append({'chunk_id':f"{x['id']}-p{number}-{start}",'paper_id':x['id'],'case_group':group,'split':split,
                'page':number,'start_char':start,'text':span,'tags':tags(span)})
    (A/'pages').mkdir(exist_ok=True)
    (A/'pages'/f"{x['id']}.json").write_text(json.dumps(page_records,ensure_ascii=False),encoding='utf-8')
    papers.append({'paper_id':x['id'],'case_group':group,'year':year,'problem_id':problem,'title':path.stem,'source_path':str(path),
        'sha256':x['sha256'],'pages':x['pages'],'split':split,'text_pages_file':f"pages/{x['id']}.json",
        'learning_status':'FULL_TEXT_INDEXED_NOT_FULL_REVIEWED','reviewed_pages':[],
        'prior_exposure':'Some excerpts of this collection were read before split; not a clean blind holdout'})
split={'created_at':datetime.now(timezone.utc).isoformat(),'unit':'year + problem; all same-question papers share split',
       'purpose':'Retrospective grouped development/evaluation; not model-weight fine-tuning or clean blind modeling test',
       'train_groups':sorted(set(p['case_group'] for p in papers if p['split']=='train')),'dev_groups':sorted(dev),'test_groups':sorted(test),
       'prior_exposure':True,'rules':['Fit retrieval statistics using train only during evaluation','Do not tune after test evaluation without versioning','Production may later search all papers; that is not held-out evaluation'],
       'papers':[{k:p[k] for k in ['paper_id','case_group','split','sha256']} for p in papers]}
for filename,obj in [('papers.json',papers),('chunks.json',chunks),('ontology.json',ontology),('split_manifest.json',split)]:
    (A/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
fingerprint=hashlib.sha256((A/'split_manifest.json').read_bytes()).hexdigest();(A/'split_manifest.sha256').write_text(fingerprint,encoding='utf-8')
print(json.dumps({'papers':len(papers),'pages':sum(p['pages'] for p in papers),'chunks':len(chunks),'split_counts':{s:sum(p['split']==s for p in papers) for s in ['train','dev','test']},'status':'Indexed; review work tracked separately'},ensure_ascii=False))
