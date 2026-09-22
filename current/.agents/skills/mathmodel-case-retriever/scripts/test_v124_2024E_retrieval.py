#!/usr/bin/env python3
from search_cases import search
r=search('高速公路 应急车道 YOLO DeepSORT TCN BiGRU 冲击波 Greenshields 摄像头布点 目标泄漏 最差组',mode='evaluation',top=20)
hits=[x for x in r['matches'] if x['case_group']=='2024-E']
ids=[x['paper_id'] for x in hits]
assert 'S020' in ids,ids
s=next(x for x in hits if x['paper_id']=='S020')
assert s['reading_status'].startswith('CORE_REVIEWED'),s
m=s.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S017','S018','S019','S020'],m
print('v1.24 2024-E S020 retrieval regression PASS')
