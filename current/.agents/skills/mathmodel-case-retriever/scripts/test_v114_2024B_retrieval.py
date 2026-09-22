from search_cases import search
r=search('WLAN MCS NSS 类别不平衡 过采样 随机森林 中间变量 双层预测 残差网络 吞吐量',mode='evaluation',top=12)
hits=[x for x in r['matches'] if x['case_group']=='2024-B']
ids=[x['paper_id'] for x in hits]
assert 'S006' in ids, ids
s6=next(x for x in hits if x['paper_id']=='S006')
assert s6['reading_status'].startswith('CORE_REVIEWED'), s6
m=s6.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S005','S006','S007','S008'], m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-B-S005-S008.json', m
print('v1.14 2024-B S006 retrieval regression PASS')
