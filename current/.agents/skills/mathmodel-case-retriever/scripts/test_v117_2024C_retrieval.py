#!/usr/bin/env python3
from search_cases import search
r=search('磁芯损耗 波形分类 Steinmetz 温度修正 ANOVA 交互作用 多目标优化 PSO 频率 磁通密度 材料 波形',mode='evaluation',top=18)
hits=[x for x in r['matches'] if x['case_group']=='2024-C']
ids=[x['paper_id'] for x in hits]
assert 'S009' in ids, ids
s9=next(x for x in hits if x['paper_id']=='S009')
assert s9['reading_status'].startswith('CORE_REVIEWED'), s9
m=s9.get('same_problem_cross_paper_map') or {}
assert m.get('papers')==['S009','S010','S011','S012'], m
assert m.get('cross_paper_map')=='knowledge_base/cross_paper_maps/2024-C-S009-S012.json', m
print('v1.17 2024-C S009 retrieval regression PASS')
