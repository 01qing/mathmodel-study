#!/usr/bin/env python3
from search_cases import search
r=search('磁芯损耗 波形 FFT 峰度 Steinmetz 温度修正 效应量 IGSE CatBoost 灰狼优化 类别编码 多目标',mode='evaluation',top=20)
hits=[x for x in r['matches'] if x['case_group']=='2024-C']
ids=[x['paper_id'] for x in hits]
assert 'S010' in ids, ids
s10=next(x for x in hits if x['paper_id']=='S010')
assert s10['reading_status'].startswith('CORE_REVIEWED'), s10
m=s10.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S009','S010','S011','S012'], m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-C-S009-S012.json', m
print('v1.18 2024-C S010 retrieval regression PASS')
