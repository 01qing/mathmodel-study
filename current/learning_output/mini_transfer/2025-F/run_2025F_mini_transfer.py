from pathlib import Path
import json, math
OUT=Path(__file__).resolve().parent
# Non-garden transfer fixture: a warehouse inspection route on a graph.
# Built after 2025-F learning: mechanism test, not clean blind capability evidence.
adj={
 'S':{'A','C'}, 'A':{'S','B'}, 'B':{'A','E'},
 'C':{'S','D'}, 'D':{'C','E'}, 'E':{'B','D','T'}, 'T':{'E'}
}
parents=[['S','A','B','E','T'],['S','C','D','E','T']]
def valid(path):
    return path[0]=='S' and path[-1]=='T' and all(v in adj.get(u,set()) for u,v in zip(path,path[1:]))
def invalid_edges(path):
    return [(u,v) for u,v in zip(path,path[1:]) if v not in adj.get(u,set())]
# First implementation: arbitrary positional one-point crossover, mirroring the risky claim.
theta=2
child_naive=parents[0][:theta]+parents[1][theta:]
first={
 'fixture':'warehouse-inspection-route', 'parents':parents, 'theta':theta,
 'child':child_naive, 'invalid_edges':invalid_edges(child_naive),
 'status':'PASS' if valid(child_naive) else 'FAIL',
 'diagnosis':'arbitrary positional crossover does not preserve graph adjacency; node-sequence length compatibility is not path feasibility'
}
(OUT/'first_fail.json').write_text(json.dumps(first,indent=2),encoding='utf-8')
# Repair rule: crossover only at a common path vertex, then replay every edge on decoded child.
commons=[v for v in parents[0][1:-1] if v in parents[1][1:-1]]
assert commons==['E']
pivot='E'
i=parents[0].index(pivot); j=parents[1].index(pivot)
child_fixed=parents[0][:i]+parents[1][j:]
second={
 'rule_change':'path-preserving splice at shared vertex + final decoded-edge replay',
 'pivot':pivot,'child':child_fixed,'invalid_edges':invalid_edges(child_fixed),
 'status':'PASS' if valid(child_fixed) else 'FAIL'
}
# Supplementary scale-contract fixture for similarity: mixed units make raw cosine concentrate.
A=[10000.,5.,0.8,0.2]
B=[10005.,50.,0.1,0.9] # structurally different, almost same large length coordinate
C=[13000.,6.,0.75,0.25] # structurally similar, scale-shifted length
scales=[10000.,50.,1.,1.]
def cos(x,y):
    dot=sum(a*b for a,b in zip(x,y)); nx=math.sqrt(sum(a*a for a in x)); ny=math.sqrt(sum(b*b for b in y)); return dot/(nx*ny)
raw={'A_B':cos(A,B),'A_C':cos(A,C)}
scaled={'A_B':cos([a/s for a,s in zip(A,scales)],[b/s for b,s in zip(B,scales)]),
        'A_C':cos([a/s for a,s in zip(A,scales)],[c/s for c,s in zip(C,scales)])}
second['similarity_scale_fixture']={
 'raw_cosine':raw,'scaled_cosine':scaled,
 'raw_both_above_0_999':raw['A_B']>0.999 and raw['A_C']>0.999,
 'scaled_correct_separation':scaled['A_C']-scaled['A_B']>0.25,
 'interpretation':'raw cosine concentration is not evidence of high semantic similarity; feature-block scaling restores separation in this fixture'
}
second['overall']='PASS_MECHANISM_TRANSFER_AFTER_RULE_FIX' if second['status']=='PASS' and second['similarity_scale_fixture']['scaled_correct_separation'] else 'FAIL'
(OUT/'repaired_pass.json').write_text(json.dumps(second,indent=2),encoding='utf-8')
print(json.dumps({'first':first['status'],'first_invalid_edges':first['invalid_edges'],'repaired':second['status'],'overall':second['overall'],'raw':raw,'scaled':scaled},indent=2))
