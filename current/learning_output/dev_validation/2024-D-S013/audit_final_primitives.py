"""Literal printed-code/number audits; these are not author pipeline executions."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

P=Path(__file__).resolve().parent
checks=[]
def keep(name,pages,first,diagnosis,repair,passed,**values):
    assert passed,name
    checks.append(dict(id=name,pages=pages,first=first,diagnosis=diagnosis,repair=repair,
                       retest='PASS_NAMED_CONTRACT_ONLY',values=values))

le=LabelEncoder().fit(['High','Low']); wrong=['Low','High']
keep('class_name_order',[100,102,107],dict(encoded_classes=le.classes_.tolist(),printed_names=wrong),
     'String LabelEncoder sorts High=0,Low=1; plotting names reverse meanings.',
     'Use encoder inverse_transform on model.classes_; separate numeric p107 branch is correctly named.',
     le.classes_.tolist()!=wrong and le.inverse_transform([0,1]).tolist()==['High','Low'])
counts=np.array([78,69,62,53,36,24,11,4]); names=['trend','rain','altitude','std','lon','lat','coverage','forest']
keep('importance_metric_identity',[47,101],dict(weight_ranking=names,printed_rain_percent=63.63),
     'Split counts and normalized gain can have different rankings; no shared importance_type is documented.',
     'Registry must store importance_type, normalization, model/run ID; do not equate different metrics.',
     names[int(counts.argmax())]=='trend' and abs(69/counts.sum()*100-63.63)>1,
     rain_share_of_visible_split_counts=float(69/counts.sum()*100),
     verdict='METRIC_NONCOMPARABILITY, not proof either run is numerically wrong')
coords=[(114.675,35.108),(113.464,33.899),(112.195,33.815),(112.002,33.837)]
directions=[]
for a,b in zip(coords,coords[1:]):
    directions.append(('N' if b[1]>a[1] else 'S')+('E' if b[0]>a[0] else 'W'))
keep('forest_centroid_directions',[66],dict(printed=['SW','NW','SW'],coordinate_replay=directions),
     'Second and third direction labels contradict signed coordinate changes.',
     'Derive direction from stored longitude/latitude deltas.',directions==['SW','SW','NW'])
ratio=(5635/100)/9_600_000*100
keep('wetland_threshold_units',[64],dict(printed_area_ha=5635,printed_percent=.00000587),
     'Under 9.6 million km2 denominator, the printed hectares imply a percentage 100 times the printed threshold.',
     'Keep ha to km2 and fraction to percent explicit; original national statistic remains unverified.',
     abs(ratio/.00000587-100)<.1,recomputed_percent=ratio,
     scope='Conditional internal unit audit, not validation of the external national wetland area')
frame=pd.DataFrame({'longitude':[110.],'latitude':[30.],'coverage_ratio':[1.]})
try:
    frame[0]
    failed=False
except KeyError:
    failed=True
keep('named_dataframe_columns',[83],dict(integer_lookup_raises_KeyError=failed),
     'calculate_area returns named columns but GDP caller accesses integer column labels.',
     'Use explicit named columns or a documented return type.',failed and frame['longitude'].iloc[0]==110.)
left=pd.DataFrame({'cell':['a','a'],'year':[1990,1991],'v':[10.,20.]})
right=pd.DataFrame({'cell':['a','a'],'year':[1990,1991],'w':[1.,2.]})
bad=left.merge(right,on='cell'); good=left.merge(right,on=['cell','year'],validate='one_to_one')
keep('cross_domain_panel_join_transfer',[98],dict(rows_before=2,rows_after=4),
     'The same omitted-time-key mechanism duplicates panel observations outside the geospatial setting.',
     'Join on entity and period with cardinality validation.',len(bad)==4 and len(good)==2,
     scope='DEV-informed mechanism transfer; not clean blind Core ablation or R7')
out={'scope':'S013 supplemental primitive audits, source pages are physical PDF pages',
     'checks':checks,'passed':len(checks),'author_pipeline_reproduced':False}
(P/'FINAL_PRIMITIVE_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
