"""Minimal executable audit: inherited return logic cannot be enabled unchanged."""
from solve import ROOT, RevisedSim
from historical_base import Sim
import json

records=[{'进车顺序':1,'动力':'混动','驱动':'两驱'}]
prefs={k:[4] for k in ['H2','F2','F4']}
legacy=Sim(records,1,prefs)
legacy.ret[1]=1;legacy.set_state(1,('ret',1),0);legacy.start_moves(0)
old_code=legacy.matrix_rows(1)[0][2]
assert old_code==71 and legacy.ret[1]==1
assert legacy.events[9]==[('rm',1,2,1)]
revised=RevisedSim(records,1,prefs)
revised.ret[1]=1
try:
    revised.start_moves(0)
except AssertionError as exc:
    guard=str(exc)
else:
    raise AssertionError('Expected explicit no-return guard')
report={
 'status':'AUDIT_COMPLETE_NOT_RETURN_VALIDATION',
 'legacy_probe':{'motion':'return position 1 to 2','start':0,'arrival':9,'at_second_1':old_code,
   'expected_under_revision_semantics':None,'source_still_occupied':True,
   'conclusion':'Inherited return motion preserves source occupancy/code during transit; inconsistent with revised lane semantics.'},
 'current_guard':guard,
 'decision':'Keep return disabled in delivered schedules. A new return implementation and independent visit-based replay are required.',
 'required_work':['Release source and reserve destination for return movement',
  'Represent repeat lane visits per car; current checker assumes exactly one visit',
  'Check return-end priority, return capacity, machine reservations and sampled endpoint exclusivity',
  'Compare return/no-return with equal budgets only after both pass independent replay'],
 'optimality_or_return_benefit_claim':False}
(ROOT/'results/RETURN_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
