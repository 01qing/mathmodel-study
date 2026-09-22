from search_cases import search
r=search('WLAN RSSI SINR MCS NSS 发送机会 吞吐量 随机森林 CNN',mode='evaluation',top=12)
hits=[x for x in r['matches'] if x['case_group']=='2024-B']
ids=[x['paper_id'] for x in hits]
assert 'S005' in ids, ids
s5=next(x for x in hits if x['paper_id']=='S005')
assert s5['reading_status'].startswith('CORE_REVIEWED'), s5
m=s5.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S005','S006','S007','S008'], m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-B-S005-S008.json', m
print('v1.13 2024-B S005 retrieval regression PASS')
