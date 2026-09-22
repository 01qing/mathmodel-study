#!/usr/bin/env python3
from search_cases import search
r=search('磁芯损耗 TLSEDSR WMTLMSEDSR Hilbert Huang 双谱 多因素方差 交互 Mann Whitney 遗传算法 粒子群 多目标',mode='evaluation',top=20)
hits=[x for x in r['matches'] if x['case_group']=='2024-C']
ids=[x['paper_id'] for x in hits]
assert 'S012' in ids,ids
s=next(x for x in hits if x['paper_id']=='S012')
assert s['reading_status'].startswith('CORE_REVIEWED'),s
m=s.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S009','S010','S011','S012'],m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-C-S009-S012.json',m
print('v1.20 2024-C S012 retrieval regression PASS')
