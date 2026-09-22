from search_cases import search
r=search('风电场 有功功率分配 疲劳损伤 遗传算法 卡尔曼 LSTM 通信延迟 多指标',mode='evaluation',top=12)
hits=[x for x in r['matches'] if x['case_group']=='2024-A']
ids=[x['paper_id'] for x in hits]
assert 'S004' in ids, ids
s4=next(x for x in hits if x['paper_id']=='S004')
assert s4['reading_status'].startswith('CORE_REVIEWED'), s4
m=s4.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S001','S002','S003','S004'], m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-A-S001-S004.json', m
assert s4.get('lexical_cosine',0)>0.12, s4.get('lexical_cosine')
print('v1.12 2024-A S004 retrieval regression PASS')
