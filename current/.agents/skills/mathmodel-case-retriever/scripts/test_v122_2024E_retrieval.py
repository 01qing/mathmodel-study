#!/usr/bin/env python3
from search_cases import search
r=search('高速公路 应急车道 YOLOv8 交通拥堵指数 时空集成 SVR BiGRU 最大似然 Weibull Kriging 遗传算法 摄像头布点',mode='evaluation',top=20)
hits=[x for x in r['matches'] if x['case_group']=='2024-E']
ids=[x['paper_id'] for x in hits]
assert 'S018' in ids,ids
s=next(x for x in hits if x['paper_id']=='S018')
assert s['reading_status'].startswith('CORE_REVIEWED'),s
m=s.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S017','S018','S019','S020'],m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-E-S017-S020.json',m
print('v1.22 2024-E S018 retrieval regression PASS')
