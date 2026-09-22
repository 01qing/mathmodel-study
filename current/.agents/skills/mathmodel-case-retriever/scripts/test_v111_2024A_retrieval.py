from search_cases import search
r=search('风电场 有功功率 疲劳 Pareto MPC 通信延迟 噪声 鲁棒优化',mode='evaluation',top=10)
hits=[x for x in r['matches'] if x['case_group']=='2024-A']
ids=[x['paper_id'] for x in hits]
assert 'S003' in ids, ids
s3=next(x for x in hits if x['paper_id']=='S003')
assert s3['reading_status'].startswith('CORE_REVIEWED'), s3
m=s3.get('same_problem_cross_paper_map') or {}
assert m.get('papers',[])[:3]==['S001','S002','S003'], m
assert m.get('cross_paper_map','').startswith('knowledge_base/cross_paper_maps/2024-A-S001-S00'), m
assert s3.get('lexical_cosine',0)>0.2, s3.get('lexical_cosine')
print('v1.11 2024-A retrieval regression PASS')
