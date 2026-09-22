#!/usr/bin/env python3
from search_cases import search
r=search('WLAN 吞吐量 物理公式 PHY Rate PER LSTM 时间序列 MSE MAE SINR 多干扰 MCS NSS',mode='evaluation',top=16)
hits=[x for x in r['matches'] if x['case_group']=='2024-B']
ids=[x['paper_id'] for x in hits]
assert 'S008' in ids, ids
s8=next(x for x in hits if x['paper_id']=='S008')
assert s8['reading_status'].startswith('CORE_REVIEWED'), s8
m=s8.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S005','S006','S007','S008'], m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-B-S005-S008.json', m
print('v1.16 2024-B S008 retrieval regression PASS')
