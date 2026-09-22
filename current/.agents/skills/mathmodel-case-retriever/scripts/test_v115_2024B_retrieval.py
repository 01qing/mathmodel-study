#!/usr/bin/env python3
from search_cases import search
r=search('WLAN SINR dBm mW MCS NSS 类别不平衡 Accuracy F1 吞吐量 RSSI',mode='evaluation',top=14)
hits=[x for x in r['matches'] if x['case_group']=='2024-B']
ids=[x['paper_id'] for x in hits]
assert 'S007' in ids, ids
s7=next(x for x in hits if x['paper_id']=='S007')
assert s7['reading_status'].startswith('CORE_REVIEWED'), s7
m=s7.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S005','S006','S007','S008'], m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-B-S005-S008.json', m
print('v1.15 2024-B S007 retrieval regression PASS')
