"""Materialize the completed human audit; generated ledgers are not automatic reading evidence."""
from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent; R=P.parents[1]; W=R/'v1.39-work'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def md(n,v):(P/n).write_text(v.strip()+'\n',encoding='utf-8')
source=Path(r'D:\BaiduNetdiskDownload\2024年研究生数学建模竞赛优秀论文选\2024年研究生数学建模竞赛优秀论文选\D\D24103850092.pdf')
sha=hashlib.sha256(source.read_bytes()).hexdigest()
assert sha=='a8c55b50f7be97971dc0b5844952dcbdc6929c07f52f841c0d0add83bec7628d'
if not (P/'RECOVERY_STATE_PRE_CLOSURE.json').exists():save('RECOVERY_STATE_PRE_CLOSURE.json',load(P/'RECOVERY_STATE.json'))
notes={14:'年降水统计与日均×100聚合假设核对。',19:'土地面积比例统计域未恢复，不能由单年吻合推广。',23:'降水年度量/日尺度极端概念区分。',24:'整数截断与打印round不一致；整数格不等于0.5度格。',25:'年度气温概念与Jan1代码对照。',30:'浅树解释路径；随机行拆分不能替代时空留出。',38:'分组最大值不等于单场事件极值。',43:'坡度单位与滚动降水标准差的地质含义不一致。',44:'指数指标和方向审查。',45:'熵归一化样本轴与指标轴。',46:'指数标签与真实灾害结果分开。',47:'正文重要性百分比与图F-score计数不同口径。',48:'可见浅树与另一深度树作为独立run登记。',49:'树阈值是样本内解释，不是独立灾害阈值。',51:'表5.3数值；全国输入未给空间分解链。',52:'草地0.003与表5.3草地0.020不一致。',56:'湿地预测图可见负值，比例约束未保障。',57:'SVR指标为作者报告；后续空间图目标来源待追。',58:'图5.24显示年度降水Gi*，正文称易损性预测。',59:'空间热点解释与预测指标不得互换。',60:'Local Moran图与SVR结果的run映射缺失。',63:'SDE角度/轴公式不保证正交；特征分解反例核验。',64:'土地高密度阈值来源和百分比换算；外部统计未独立验证。',66:'森林第二、第三阶段方向与经纬度增减矛盾。',67:'椭圆范围面积与实际资源面积不可混同。',68:'KDE变量是coverage_ratio，不能证明二维坐标正态。',69:'覆盖率边际分布不等于空间联合分布。',70:'同前；协方差描述与概率覆盖声明分开。',71:'一维68%规则不能直接用于二维椭圆。',72:'方向/覆盖解释应限定几何描述。',73:'用途声明需独立任务验证。',76:'人口/GDP/土地叠加支持描述，不证明独立效用提升。',79:'作者局限承认年度尺度难识别短时事件。',82:'投影/TFW定义和函数调用边界。',83:'返回命名DataFrame与整数列访问不兼容。',84:'全文件处理函数存在，调用被注释，不能认定执行。',85:'仅Jan1气温；像元中心+.1与+.5不同。',86:'round取整与正文截断不一致。',87:'降水Value乘100；不能据此认定完整Q1数据链。',88:'合并输入列名与前段输出列名不一致。',90:'回归分支存在正确train/test分开。',91:'阈值250与正文300不一致；拆分存在。',92:'该分支随后全量拟合和评估。',93:'按年最大记录不是单场事件最大。',96:'三行滚动非三年；全时期分位数/趋势有泄漏风险。',98:'terrain跨年展开后仅坐标合并，有30倍重复风险。',99:'实际五列minmax均值非正文熵权；无可见完整导入链。',100:'High/Low字符串LabelEncoder；伪标签不是真实灾害。',101:'XGB分支有训练测试拆分；重要性类型不统一。',102:'class_names顺序逆于字符串编码。',104:'按Year全国汇总未来输入。',105:'[4:5]仅湿地，ARIMA(3,0,6)17步；非六变量完整脚本。',106:'拟合误差不能替代未来回测。',107:'numeric High=1分支命名正确；实际DecisionTree而非注释XGB。',108:'SVR变量定义顺序不完整，误差变量可能陈旧；缺空间输入。',109:'人口年份链不全，范围与多年均值描述不同。',110:'人口/GDP投影返回轴顺序不一致，实际取决于版本；固定always_xy。',111:'总量栅格均值聚合需注明测度；不能当守恒总量。',112:'打印KDE覆盖率代码不构成SDE/GIS运行链。',113:'KDE绘图结尾，未见SDE、Gi*、Local Moran完整执行代码。'}
bands=[(1,12,'摘要、题目重述、数据和总体技术路线'),(13,29,'Q1时空统计、图例、土地与气候描述'),(30,42,'Q2树模型、分组关系、验证口径'),(43,60,'Q3易损性指数、预测、结果图表'),(61,79,'Q4空间摘要、椭圆、用途和局限'),(80,81,'参考文献与附录衔接'),(82,113,'打印Python代码静态审计')]
sheets={p:f"visual/sheets/{s['sheet']}" for s in load(P/'visual/sheets/index.json') for p in s['pages']}
ledger=[]
for p in range(1,114):
    section=next(t for a,b,t in bands if a<=p<=b)
    ledger.append({'physical_page':p,'printed_page':p-1 if p>1 else None,'text_review':'COMPLETED','visual_review':'COMPLETED',
                   'visual_evidence':sheets.get(p,f'visual/p{p:03}.png'),'topic':section,
                   'note':notes.get(p,'已检查本页正文、可见公式、图表/图例或代码；结论按所在问题的证据链登记，不单凭本页赋予验证通过。')})
save('PAGE_AUDIT_LEDGER.json',{'source_sha256':sha,'total_pages':113,'visual_count':113,'text_count':113,
      'basis':'Assistant actually inspected original-PDF renders and extracted text over continued turns; page images alone do not prove review.',
      'precision_limit':'Contact sheets support page/layout review; only legible values transcribed. Unresolved small labels are not invented.',
      'printed_code_static_pages':list(range(82,114)),'pages':ledger})

entries=[]
def entry(i,q,pages,value,units,status,scope,evidence,missing=''):
    entries.append(dict(paper_id='S013',question=q,result_id=i,source_surface={'physical_pdf_pages':pages},value_or_record=value,
                        units=units,status=status,verification_scope=scope,evidence_file=evidence,missing_for_full_reproduction=missing,
                        run_id='AUTHOR_RUN_UNAVAILABLE',evaluator_id='UNAVAILABLE_UNLESS_EXPLICIT_IN_VALUE'))
agg=load(P/'Q1_AGGREGATION_RESULTS.json')
for a in agg['precipitation']:
    entry('Q1-PRE-'+str(a['year']),'Q1',[14],a,'paper mm; alternative contracts explicitly recorded','partially_verified',
          'Official raw data daily mean times100 matches at2dp; annual-total interpretation not supported. No author workbook/GIS reconstruction.',
          'Q1_AGGREGATION_RESULTS.json','Author aggregation script, workbook, crop boundary')
for a in agg['cropland']:
    entry('Q1-CROP-'+str(a['year']),'Q1',[19],a,'percent','not_reproducible_from_visible_evidence','Positive-cell mean hypothesis does not recover all3values.',
          'Q1_AGGREGATION_RESULTS.json','Author support domain and spatial weights')
records=[
('Q1-TEMP','Q1',[25,85],{'Jan1_C':-8.593109,'annual_C':6.875655,'MAE_C':15.468764},'degC','partially_verified','Official-data counterexample; not author workbook reproduction.','COUNTEREXAMPLE_RESULTS.json'),
('Q2-TARGET','Q2',[23,34,91,93],'annual thresholds300/250 and annual maxima do not identify daily extremes','mm with incompatible temporal support','contradicted','Target-definition conflict.','COUNTEREXAMPLE_RESULTS.json'),
('Q2-SPLIT','Q2',[90,91,92],'Some branches split correctly; p92 evaluates full fitting data','validation contract','partially_verified','Static branch-specific audit; do not generalize to all branches.','PAGE_AUDIT_LEDGER.json'),
('Q3-MERGE','Q3',[98],{'fixture_input':2,'bad_rows':60,'fixed_rows':2},'rows','recomputed_verified','Conditional duplicate-join mechanism only.','COUNTEREXAMPLE_RESULTS.json'),
('Q3-ENTROPY','Q3',[45,99],'printed entropy formula vs five-feature minmax mean','index','contradicted','Formula normalization counterexample; printed code does not execute entropy weighting.','COUNTEREXAMPLE_RESULTS.json'),
('Q3-PSEUDOLABEL','Q3',[100,101],'V_index threshold defines label from input-derived index','class','partially_verified','Accuracy measures imitation, no independent disaster outcome.','COUNTEREXAMPLE_RESULTS.json'),
('Q3-IMPORTANCE','Q3',[47,101],{'rain_text_percent':63.63,'visible_rain_split_count':69,'visible_trend_split_count':78},'gain/weight unspecified','not_reproducible_from_visible_evidence','Different metrics may both be valid; need importance_type and run linkage.','FINAL_PRIMITIVE_RESULTS.json'),
('Q3-LABELS','Q3',[100,102,107],{'string_branch':['High','Low'],'plotted':['Low','High'],'numeric_p107':'correct'},'class order','contradicted','Only string-encoded branch is reversed.','FINAL_PRIMITIVE_RESULTS.json'),
('Q3-LAND-TABLE','Q3',[51,52],{'grass_table2020':.020,'forest_table2020':.003,'grass_prose2020':.003},'fraction','contradicted','Table/prose identity conflict; neither supplies original model arrays.','SPATIAL_PROVENANCE_RESULTS.json'),
('Q3-SVR-TRAIN','Q3',[57,108],{'MSE':.0029,'MAE':.0443,'R2':.8579},'index squared/index/dimensionless','author_reported','MSE>=MAE² sanity only; data and runnable chain absent.','PAGE_AUDIT_LEDGER.json'),
('Q3-SVR-TEST','Q3',[57,108],{'MSE':.0029,'MAE':.0442,'R2':.8565},'index squared/index/dimensionless','author_reported','Cannot independently replay original evaluation.','PAGE_AUDIT_LEDGER.json'),
('Q3-SPATIAL','Q3',[51,104,108],{'same_inputs_prediction_range':0.0},'index','partially_verified','Conditional invariant; missing regional future inputs prevents recovery of spatial output.','SPATIAL_PROVENANCE_RESULTS.json'),
('Q3-FIGURE-IDENTITY','Q3',[57,58,59,60],{'prose':'SVR vulnerability','figure':'annual precipitation Gi* / Local Moran'},'different target/statistic','contradicted','Result-source mismatch; no replacement numbers invented.','SPATIAL_PROVENANCE_RESULTS.json'),
('Q3-FORECAST','Q3',[56,105,106],'Only wetland forecast slice printed; negative future values visible; fitted errors not forecast validation','fraction','not_reproducible_from_visible_evidence','Qualitative plot and code audit; missing all-six-variable run and prediction intervals.','PAGE_AUDIT_LEDGER.json'),
('Q4-AXES','Q4',[63],{'printed_axis_dot':.9230769231,'fixed_crosscov':1.6208867e-16},'fixture units','recomputed_verified','Literal formula counterexample/eigendecomposition repair, not GIS reproduction.','SPATIAL_PROVENANCE_RESULTS.json'),
('Q4-AREA','Q4',[67],'doubling total weights leaves covariance ellipse unchanged','area vs distribution extent','recomputed_verified','Counterexample to equating ellipse area with resource area.','COUNTEREXAMPLE_RESULTS.json'),
('Q4-COVERAGE','Q4',[68,69,70,71],{'2D_mass_radius1':.39346934,'2D_mass_radius_sqrt2':.63212056},'probability conditional on Gaussian','recomputed_verified','Dimension-specific analytic contract; not measured author empirical coverage.','COUNTEREXAMPLE_RESULTS.json'),
('Q4-DIRECTION','Q4',[66],{'printed':['SW','NW','SW'],'replay':['SW','SW','NW']},'direction','contradicted','Signed coordinate replay for forest only.','FINAL_PRIMITIVE_RESULTS.json'),
('Q4-WET-THRESHOLD','Q4',[64],{'printed_percent':.00000587,'conditional_percent':.0005869791667},'percent','partially_verified','Conditional unit mismatch; external statistic5635ha unverified.','FINAL_PRIMITIVE_RESULTS.json'),
('Q4-UTILITY','Q4',[74,75,76,77,78,79],'geographical line proposed by overlays','descriptive claim','author_reported','No independent downstream utility comparison; do not adopt as optimum.','DEV_METHOD_GAP_REVIEW.md')]
for v in records:entry(*v,missing='Author executable intermediates and complete run provenance unavailable')
save('S013_RESULT_REGISTRY.json',{'schema_version':'1.0','paper_id':'S013','split':'dev','scope':'Audited key claims across all four questions, not an exhaustive transcription of every plotted pixel.',
     'entries':entries,'unresolved_policy':'Keep conflicts/unverified claims; no automatic promotion to verified.','independent_baseline_registry':'../../v1.39-work/learning_output/analyses/dev_2024D_presolution/results/RESULT_REGISTRY.json'})

common={
'input_data_and_independent_unit':'Official raster/cell-year with explicit temporal support; repeated cover-type rows are not independent observations. Freeze predates S013 access.',
'validation_protocol':'Use frozen pre-S013 independent evidence for baseline; any additional diagnostics are Dev-informed. No causal or clean-blind Core gain inference.',
'failure_and_abandon_conditions':'Reject target/unit/join leakage; discard complex model without stable material holdout gain; retain unresolved provenance.',
'recommended_rebuild':'Implement minimal primitive with declared units/support, independent validation, run IDs and replayable results; do not copy author thresholds.',
}
specs={
'Q1':dict(problem_type_and_essence='多源气候与土地覆盖的描述统计；关键在时间聚合与空间测度。',target_and_constraints='年累计降水、年均温、面积比例；共同有效域、缺失年不伪造。',author_method_chain='栅格转点/整度汇总、GIS地图、均值极值与趋势。',why_author_method_fits='描述统计和地图能展示空间差异，前提是支持域和单位一致。',baseline='原始网格有效域面积加权年统计',alternatives=['分区分位数与稳健趋势','有来源边界的面积相交守恒汇总'],avoid='以平滑插值图反算总量；日均×100称年累计',choice='保留网格统计，GIS只作为有边界证据的表达模块',switch='裁剪来源和守恒误差经过验证才升级空间精度',six_hour_baseline=['1小时核对单位、缺失和年份','2小时共同域面积权重与年度聚合','1小时趋势/分位数','1小时3张以内核心图','1小时跨表核对与限制说明'],data_to_model_mapping='daily precipitation→sum/year；daily temperature→mean/year；cell_area×cover_fraction→resource area。',assumptions_formulas_parameters='P_y=sum_day P；mean_area=sum(w*x)/sum(w)；nodata≠0。',code_paper_mapping='pp82–89；Jan1路径、round、Value×100和列名缺失映射。',figure_decisions='选择趋势/空间格局/土地变化；每图附单位、年份、分母和nodata。',result_metrics='降水5/5聚合假设吻合，耕地3年未完整恢复；见Registry。',cross_surface_consistency='年/日尺度、温度Jan1/年均、整数格/0.5度格不一致。',risks_and_errors='空间支持域、分母选择、重采样非守恒。',applicability='多源栅格描述与官方统计审计。',transferable_modules=['单位与时间支持合同','面积守恒聚合']),
'Q2':dict(problem_type_and_essence='极端降水预测与地形气候交互解释，应区分预测、描述和因果。',target_and_constraints='以Rx1/Rx5日尺度目标比较；时间/空间独立单位，不用年累计替代暴雨。',author_method_chain='树回归/分类、分组阈值和相关关系；代码有正确拆分及全量拟合不同分支。',why_author_method_fits='浅树便于解释非线性与交互，但阈值需分块稳定性检验。',baseline='气候态预测＋地形温度分层描述',alternatives=['加性与交互回归同切分对比','浅树或HGB配合分块重采样'],avoid='随机重复行划分、高拟合分数称因果机理',choice='保留冻结气候态；复杂候选时间验证未胜出',switch='时空留出稳定实质改善，且交互方向/阈值跨块稳定',six_hour_baseline=['1小时目标和时间合同','1小时气候态','2小时加性/交互/浅树同切分','1小时分块误差与分层图','1小时限制和误差审计'],data_to_model_mapping='cell-year日极值←DEM/relief/temperature；土地不替代地形。',assumptions_formulas_parameters='冻结气候态、加性/交互与HGB；新解释检验未执行。',code_paper_mapping='pp90–98；p92全量拟合只归该分支；坐标合并与三行rolling有风险。',figure_decisions='留出误差、分层关系、残差空间图；不以单树图证明机制。',result_metrics='冻结验证MAE气候态9.52876，HGB10.15481；复杂模型不升级。',cross_surface_consistency='250/300年阈值不一致；年度最大记录非单场极值。',risks_and_errors='时间泄漏、空间相关、伪重复、因果过度解释。',applicability='有明确目标和留出合同的环境回归及解释。',transferable_modules=['实体-时间合并验证','解释稳定性门槛']),
'Q3':dict(problem_type_and_essence='未来成灾风险应拆分危险度、暴露与易损性，识别无标签限制。',target_and_constraints='无独立灾损标签只能情景指数/排序；比例非负且有定义。',author_method_chain='易损性指数→伪标签树/XGB→ARIMA未来输入→SVR→空间分析。',why_author_method_fits='分层指数具有组织价值，预测链必须有区域输入和真实评价支持。',baseline='持续性中心情景＋显式风险假设与多情景范围',alternatives=['区域化输入与滚动回测','有真实灾损标签后的时空校准模型'],avoid='伪标签准确率当灾害预测精度；全国输入直接生成空间图',choice='保留冻结36情景，标注假设；不导入作者阈值或SVR精度',switch='独立灾害标签、区域输入、优于持续性的回测三项齐备',six_hour_baseline=['1小时分开H/E/V与数据缺口','1小时持续性对照','2小时少量可解释情景','1小时敏感性和排序稳定性','1小时注册假设与不确定性'],data_to_model_mapping='历史统计→未来情景，不把预测量当观测；伪标签与灾损标签分栏。',assumptions_formulas_parameters='作者ARIMA(3,0,6)仅可见湿地分支；minmax平均≠熵权；>.37为指数阈值。',code_paper_mapping='pp99–108；LabelEncoder类别顺序、旧变量、无空间输入和不完整六变量链。',figure_decisions='情景范围与非负约束检查；Gi*/LocalMoran不可替代SVR预测图。',result_metrics='作者SVR train/test R2 .8579/.8565未复现；MSE/MAE仅通过必要算术条件。',cross_surface_consistency='grass .003/.020；预测目标与空间图标题不同；重要性gain/weight不可直接比较。',risks_and_errors='自生成目标泄漏、跨年特征泄漏、run来源混淆、无约束外推。',applicability='缺少观测标签时的透明情景分析；不适用于已校准概率宣称。',transferable_modules=['标签来源登记','结果身份与run追溯','未来输入空间支持合同']),
'Q4':dict(problem_type_and_essence='土地结构压缩、地理摘要与用途评价是三个不同任务。',target_and_constraints='重建误差/时间稳定性/下游用途分别验证；空间面积用合适投影。',author_method_chain='阈值筛选→重心/SDE→人口GDP降水叠加→地理界线。',why_author_method_fits='重心和方向便于沟通，不能把椭圆范围视为土地总面积或最优界线。',baseline='冻结K=5土地结构分区＋重建误差和时间稳定性',alternatives=['面积加权重心与协方差摘要','独立下游任务对比K分区、单区、经纬度简单分区'],avoid='一维68%用于二维；用参与选线数据重复验证用途',choice='冻结K分区保持，SDE仅候选描述模块',switch='七门合同满足且独立用途有稳定实质提升才组合',six_hour_baseline=['1小时覆盖率测度审计','2小时K分区与单区/PCA对照','1小时空间重建及窗口稳定性','1小时重心/分区图','1小时用途边界和报告'],data_to_model_mapping='w=cell_area×cover_fraction；投影坐标→加权中心/协方差；单独sum(w)。',assumptions_formulas_parameters='eigh对称协方差；概率覆盖须明确维度/分布，普通描述不要求正态。',code_paper_mapping='pp109–113仅人口/GDP汇总及coverage_ratio KDE，缺SDE/Gi*/LocalMoran可运行链。',figure_decisions='分区图、误差图、描述椭圆；覆盖率KDE不能验证二维坐标正态。',result_metrics='冻结K5空间RMSE .07583，单区 .15134，PCA2 .08154；独立下游效用尚未建立。',cross_surface_consistency='森林方向两处矛盾；湿地阈值条件换算100倍；年份/统计变量有漂移。',risks_and_errors='度与公里混用、面积概念替代、事后选线、混合分布过度解释。',applicability='可解释空间摘要；需要独立用途才能作决策建议。',transferable_modules=['正交主轴与面积分账','下游用途独立验证门槛'])}
cards={}
for q,s in specs.items():
    card=dict(common)
    for k,v in s.items():
        if k not in ['baseline','alternatives','avoid','choice','switch']:card[k]=v
    card['candidate_model_competition']={'baseline':s['baseline'],'author_route':s['author_method_chain'],'major_alternatives':s['alternatives'],
      'not_recommended':s['avoid'],'why_select':s['choice'],'why_not_select_author_as_default':'原始执行链和独立优势证据不全，且已识别目标/单位/来源问题。','switch_conditions':s['switch']}
    cards[q]=card
save('S013_QUESTION_CARDS.json',{'paper_id':'S013','case_group':'2024-D','split':'dev','source':str(source),'source_sha256':sha,
      'reproduction_level':'R2','visual_audit':'113/113 separately recorded','question_cards':cards,'core_promoted':False})
gates=[
('输入输出接口','BLOCKED_AUTHOR_OUTPUT_IMPORT','缺作者中间表/GIS输出；重建需cell_id/year唯一键及cardinality。'),
('变量定义','BLOCKED_DIRECT_COMPOSITION','年降水/日极值、风险/易损性、覆盖率/面积、gain/weight不能互换。'),
('数据分布','BLOCKED_DIRECT_COMPOSITION','裁剪域及空间解聚合未知；统一年份和留出后再比较。'),
('数学假设','REPAIR_SPECIFIED_NOT_END_TO_END_VALIDATED','二维覆盖率和正交轴局部反例已复测；不等于作者GIS已修复。'),
('量纲','REPAIR_SPECIFIED_NOT_END_TO_END_VALIDATED','面积权重、投影、ha/km²/%须显式；外部湿地总量未核实。'),
('训练/执行阶段','FROZEN_BASELINE_PROTECTED_CANDIDATE_PENDING','冻结方案不回填；阈值/标准化/选线必须在训练数据完成。'),
('评价指标','BLOCKED_FOR_RECOMMENDATION','当前无独立下游效用/真实灾损优势；复杂模型不能进入推荐主线。')]
save('S013_METHOD_MAP_AND_COMPOSER.json',{'status':'FINAL_S013_VS_FROZEN_BASELINE_ONLY','group_final':False,
      'papers_reviewed':['S013'],'papers_not_opened':['S014','S015','S016'],
      'questions':{q:c['candidate_model_competition'] for q,c in cards.items()},
      'proposed_composition':'冻结分区＋面积加权空间摘要＋独立用途评价',
      'seven_gates':[dict(gate=a,status=b,reason=c) for a,b,c in gates],
      'decision':'DO_NOT_IMPORT_AUTHOR_OUTPUTS_OR_PROMOTE_COMPOSITE_YET',
      'scope':'All seven gates examined. Not all seven passed. Full case-group map/transfer awaits authorized remaining Dev reviews.'})
save('S013_MODULES_AND_ERRORS.json',{'split':'dev','promotion':'CANDIDATE_ONLY',
      'modules':[{'question':q,'modules':c['transferable_modules'],'entry_condition':c['applicability'],
                  'reject_condition':c['failure_and_abandon_conditions'],'status':'LOCAL_CONTRACTS_TESTED_WHERE_REFERENCED; INTEGRATED_GAIN_NOT_ESTABLISHED'} for q,c in cards.items()],
      'error_patterns':[{'question':q,'patterns':c['risks_and_errors'],'evidence':'S013_RESULT_REGISTRY.json'} for q,c in cards.items()],
      'mini_transfer':{'status':'DEV_INFORMED_MECHANISM_ONLY','fixture':'cross_domain_panel_join_transfer','evidence':'FINAL_PRIMITIVE_RESULTS.json',
                       'history':'2 rows→4 duplicated rows (FAIL); add entity+period keys→2 rows (PASS contract only)',
                       'full_case_group_transfer':'NOT_DUE; S014-S016 not read','R7':False,'core_gain':'NOT_ESTABLISHED'}})
md('S013_CODE_FIGURE_AUDIT.md','''
# S013 代码、公式与图表最终审计

原PDF物理页113页；正文及图表113/113已读；附录82–113页打印Python静态审计完成。页码均为物理页，纸面页码通常小1。详细逐页账本见 PAGE_AUDIT_LEDGER.json；全部关键结果见 S013_RESULT_REGISTRY.json。

Q1：82–89页栅格、投影、聚合和表格拼接。calculate_area 返回命名DataFrame而调用方按整数列取值；TFW函数存在中心/角点及参数顺序风险，但未见调用证据，不声称污染所有输出。气温全文件函数调用被注释，另一路仅Jan1；降水Value×100与表中数字一致的聚合假设不代表恢复作者完整过程。输入输出列名还缺重命名链。地图适合描述，不能替代面积守恒统计。

Q2：90–98页浅树/回归、年度目标、rolling和合并。必须按分支评价：90–91页可见正确训练测试拆分，92页另一路全数据拟合/评分。年度累计250/300阈值不是日极端；三行rolling不等于三年；terrain跨30年展开后仅坐标合并可能放大30倍。正文浅树可解释，但不构成因果识别。

Q3：99–108页实际minmax五列平均，与正文熵权不是同一算法。High/Low伪标签来自指数，预测精度不能验证灾害。字符串编码分支High=0却绘制Low=0；107页数值High=1分支是正确的，不能一概判错。XGB分支有真正训练测试拆分。正文重要性百分比与图中weight计数要分别记录，排名不同本身不证明错误。ARIMA只打印[4:5]湿地切片，拟合误差不等于回测；负预测未见约束。SVR存在定义顺序/陈旧误差变量和中间表缺失，无法重放原run。全国年度六变量输入不带空间差异时，同年SVR输出不能自动形成空间差异；Gi*/LocalMoran降水图与所称易损性输出身份不同。

Q4：109–113页人口/GDP聚合和覆盖率KDE。投影返回值两段顺序不同，须锁定pyproj版本或always_xy后核验，不能不加条件断言是哪段反了。2015人口/2014GDP示例不构成1990–2020多年链。总量格网取均值不保证资源守恒。打印代码无完整SDE、Gi*、LocalMoran或椭圆内叠加实现。正文协方差主轴公式与正交性不符，局部特征分解修复已验证；并未执行作者GIS。覆盖率KDE不是二维坐标分布检验；一维68%不能直接解释二维椭圆，椭圆面积不是资源总面积。森林方向有两处符号矛盾，外部湿地统计缺来源核验。

图表决策：Q1保留少量单位清楚的趋势/空间格局；Q2画独立误差和分层关系；Q3画情景范围并记录目标、统计量、run和输入预测版本；Q4分别画分区、误差与描述性空间摘要。不得以视觉平滑、方向吻合或高拟合分数证明模型提升。

复现等级依据冻结 schema reproduction_levels_v1.json：R1全文、R2打印代码静态审计已经满足，故 S013=R2。作者工程源码、原中间工作簿、完整GIS调用及参数/输出未取得；未执行作者完整代码smoke，不达到R3。局部真实数据聚合和合成反例不把整篇提高到R4–R7。视觉审查单独记录。没有可运行作者代码包，audit_code_bundle 对作者包的执行为 NOT_APPLICABLE；未将OCR拼接为可执行作者源码冒充复现。
''')
print('Wrote S013 audit assets; closure state awaits executed validation.',flush=True)
