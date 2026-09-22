#!/usr/bin/env python3
from search_cases import search
r=search('高速公路 应急车道 YOLOv10 ByteTrack ARIMA AdaBoost 十分钟密度预测 区间车辆占有率 0.8 0.6 车道热度图 摄像头布点',mode='evaluation',top=20)
hits=[x for x in r['matches'] if x['case_group']=='2024-E']
ids=[x['paper_id'] for x in hits]
assert 'S019' in ids,ids
s=next(x for x in hits if x['paper_id']=='S019')
assert s['reading_status'].startswith('CORE_REVIEWED'),s
m=s.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S017','S018','S019','S020'],m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-E-S017-S020.json',m
print('v1.23 2024-E S019 retrieval regression PASS')
