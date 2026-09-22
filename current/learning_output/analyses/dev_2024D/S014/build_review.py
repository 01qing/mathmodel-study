from pathlib import Path
import json,datetime,hashlib
O=Path(__file__).resolve().parent;W=O.parents[3]
def dump(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def md(n,x):(O/n).write_text(x.strip()+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
replay=json.loads((O/'AUDIT_REPLAY.json').read_text(encoding='utf-8'))
assert replay['status']=='PASS'
access=json.loads((O/'ACCESS_EVENT.json').read_text(encoding='utf-8'))
access.update(full_text_review=True,visual_review=True,R_level='R2',completed_at=now,visual_scope='62/62 original PDF pages inspected as115dpi two-page renders, not pixelwise replication of every plotted value',static_code_scope='PDF53–62: Sen, MK, RF, XGB; no original end-to-end pipeline executed')
dump('ACCESS_EVENT.json',access)
page_notes={
1:'Cover and source identity; award not externally verified',2:'Abstract Q1–Q4 claims',3:'Contents Q1–Q4',4:'Contents audit appendix locator',5:'Problem restatement and independent samples assumption',6:'Assumptions, Q1 flow',7:'Daily precipitation support and TIFF conversion',8:'Calendar aggregation and incompatible stated grid resolution/shape',9:'Annual precipitation plot, units and time-scope ambiguity',10:'SD plot spatial/time axis and caption2022 vs2020',11:'Pearson association and MK signed-pair sum',12:'Eq3-10 denominator30 visually confirmed',13:'MK significance table and map; percentages rounded',14:'Sen slope and overlapping Table3-5 classes',15:'Land fractions and relative change formula',16:'Average change rates, fraction/percent labels',17:'Five land mean maps; prose ordering reversed',18:'Five change maps; no independent impact truth',19:'Q2 feature and dataset contracts',20:'Slope/aspect formula and0east clockwise convention; slope units unresolved',21:'1979–2018temperature vs1961–2022caption; daily rain thresholds',22:'Cellwise elevation/rain scatter',23:'Binned totals require exposure denominator',24:'Slope60–90degree map anomaly requires pipeline trace',25:'Slope/aspect heatmap and temperature scatter',26:'Temperature bins; correlation not causal',27:'DEM/slope/aspect correlations0.98; derivation alone insufficient explanation',28:'Multiple targets and R2/MSE definitions',29:'Nested elevation cohorts; different test populations',30:'Temperature subgroups and changed target variance',31:'Target-conditioned Rainfall selection; separate tasks',32:'ML competition and CV claims',33:'RF/XGB table and prose1613.645 vs1612.645',34:'Importance semantics; DEM derived drainage starts',35:'MK-gated Sen future extrapolation; no hindcast shown',36:'Critical conditions omit calibrated precipitation/disaster target',37:'HEV multiplication and indicators',38:'AHP reciprocal matrix vs sum1 conflict',39:'AHP table normalization primitive; CI/CR and entity mapping; WeightedSum',40:'Risk map and southeast qualitative interpretation',41:'Northeast and western map comparisons',42:'Western interpretation, Q4 data supports',43:'Three terrain steps qualitative map',44:'800mm map uses annual totals unlike Q1 daily mean; no numeric lineage',45:'Geographical overlays; map appearance not external validation',46:'Land positive/negative rate correlations; sign definitions unresolved',47:'Land/GDP/population heatmaps; identical/opposite correlations need input trace',48:'Forest/shrub/wetland heatmaps; inspect axis names',49:'Table6-3 crop miscalled shrub; MSE direction typo; population-altitude sign contradiction',50:'Predictions and future maps; driver forecasts not supplied',51:'Interpretation and self-evaluation',52:'Limits and references, more models not automatic improvement',53:'References and Sen initialization',54:'Sen loop excludes zeros; original indentation valid unlike extraction',55:'MK uses18 without ties; flattened mask into2Dzc',56:'RF raster read drops metadata; author intermediate paths',57:'zoom by shape, linear cyclic aspect, dropna only',58:'RF random80/20 with5foldCV; not stated60/20/20',59:'RF plot regression line is not identity line; XGB begins',60:'XGB same raster alignment problems',61:'XGB random80/20 and3foldCV; different search budget',62:'XGB outputs; no Q3/4 full executable appendix'}
dump('PAGE_AUDIT_LEDGER.json',dict(source_sha256=access['source']['sha256'],pages=[dict(pdf_page=i,printed_page=i-1,text_reviewed=True,visual_reviewed=True,image=f'visual/pages_{i if i%2 else i-1:02d}_{i+1 if i%2 else i:02d}.png',note=page_notes[i]) for i in range(1,63)],visual_does_not_raise_R=True))
registry=[]
def reg(i,q,p,loc,claim,status,diagnosis,action,link=None):
    registry.append(dict(result_id=f'S014-{i:02d}',paper_id='S014',split='dev',question=q,pdf_pages=p,locator=loc,author_claim=claim,audit_status=status,diagnosis=diagnosis,decision=action,replay=link,run_id='author_unavailable',input_version='author_intermediates_unavailable',review_run='S014-local-audit-20260913',author_result_reproduced=False))
reg(1,'Q1',[8],'Eq3-1..3','月均→季均→年均','LOCAL_COUNTEREXAMPLE','月均值等权与逐日均值不同；日均mm与年累计mm分开','使用有效日数加权，登记聚合轴','calendar')
reg(2,'Q1',[8],'Table3-3','0.5degree and144x256','INTERNAL_METADATA_CONFLICT','与所列经纬度跨度不相容；作者未提供重采样链','用官方栅格transform/shape核验，不直接采信表')
reg(3,'Q1',[9,10,53,55],'1990–2020/2022 captions;range1990,2020','覆盖1990–2020','CODE_SCOPE_CONFLICT','代码仅1990–2019；正文图有2020；不能假定同一run','显式time_start/end/inclusive/valid_count')
reg(4,'Q1',[12,55],'Eq3-10 vs MK.py','MK variance numerator/30 vs/18','EXACT_NULL_REPLAY','7distinct值5040排列方差44.333333；/30为26.6','采用18并处理ties；作者地图来源未恢复','MK denominator')
reg(5,'Q1',[14],'Table3-5','五类趋势划分','LOCAL_COUNTEREXAMPLE','beta=.001,Z=0同时满足增强和不变','先定义互斥effect区间，再独立登记显著性；不反推作者百分比','partition_witness')
reg(6,'Q1',[13,14],'Tables3-4/5','27.44/70.99/1.56等比例','UNREPRODUCED','仅表格/图可核对；小于0.03pp总和偏差可为四舍五入','保留报告值，不将作者地图判全面错误')
reg(7,'Q1',[54,55],'positive-only guard','np.min(data)>0 / all(data>0)','STATIC_CONFIRMED','把有效零值和缺失值混合；mask需要产品合同','零值保留，NoData显式处理')
reg(8,'Q1',[55],'sresult andzc shapes','一维布尔条件赋值二维数组','EXECUTED_LOCAL_FAILURE','2x3 fixture实际IndexError；已验证flat→reshape修复','修复只证明数组合同，不等于作者MK图复现','shape_exception')
reg(9,'Q2',[20,24,36],'slope/aspect','大面积60–90degree；0east clockwise','UNRESOLVED_PIPELINE','图与文字确有该范围，但缺DEM导数脚本，不能断定具体单位错误','核验水平距离单位、角度零点和方向；不用此阈值作通用规则')
reg(10,'Q2',[21],'Fig4-3','1961–2022年均温','SUPPORT_CONFLICT','该页声明输入1979–2018；无外推链','未来/历史共同支持需登记')
reg(11,'Q2',[23,26],'binned sums','总次数最多说明发生倾向最高','DENOMINATOR_GATE','总量同时受样本数/有效日/面积影响','统计率时保留exposure；并非否认总量图本身','exposure')
reg(12,'Q2',[27,47,48],'correlation heatmaps','terraincorr.98;GDP/popcorr−1','UNRESOLVED_INPUT_PROVENANCE','数值可见；从同一DEM派生不推出.98；不能无证断言重复列','检查逐行entityid、列hash、反向编码和mask后才解释')
reg(13,'Q2',[29,30,31],'Tables4-3..6','分区模型R2更高代表模型更好','INCOMPARABLE_COHORTS','嵌套区域、不同Y筛选改变评价总体；目标条件不能用于未知Y路由','共同heldout集合比较，目标条件仅事后分层诊断')
reg(14,'Q2',[33],'Table4-7/prose','XGB MSE1613.645/1612.645','RESULT_SOURCE_CONFLICT','两处差1；表RF1620.793；按表相对改善.4410187%','无相同阻塞验证和种子稳定性，不提升为推荐主线','Q2_table_gain_percent')
reg(15,'Q2',[34],'Fig4-20','温度importance.829/.814','NOT_CAUSAL_EVIDENCE','树重要性不同实现口径，相关地理特征可替代；无因果识别','登记importance_type、normalization与外部结果')
reg(16,'Q2',[56,57,60],'read_raster/zoom','相同形状完成地理对齐','STATIC_CONTRACT_FAILURE','丢crs/transform/nodata；shape ratio zoom不是地理重投影；坡向周期插值错误','对齐坐标、网格和mask，坡向用sin/cos向量')
reg(17,'Q2',[29,58,61],'train/CV split','60/20/20 vs80/20+CV','CODE_CONTRACT_DIFFERENCE','打印RF5fold,XGB3fold；随机空间划分，非时空外推验证','保留不同任务可能不同划分，要求逐表run_id而不泛化全部泄漏')
reg(18,'Q3',[35],'Fig5-2','MK显著才做Sen外推','CANDIDATE_UNVALIDATED','统计显著不保证未来更准；缺rolling hindcast；未来驱动不齐','在共同滚动窗口与持久性竞争后才晋级')
reg(19,'Q3',[36],'Table5-1','暴雨成灾临界条件','TARGET_NOT_CALIBRATED','给出高程/坡度/坡向/温度/土地类型，没有可验证降雨-损失边界','仅描述危险条件；不称真实成灾阈值')
reg(20,'Q3',[37,39],'Eq5-1 vs5.4.3','HEV product vsArcGISWeightedSum','OPERATOR_DRIFT','乘积和加权和可产生排名反转','两模型分别命名并验证，不能只换实现沿用结论','HEV_counterexample')
reg(21,'Q3',[38,39],'Eq5-2 andTable5-5','判断矩阵sum1及互反','INTERNAL_CONTRACT_CONFLICT','正互反矩阵对角为1，不可整体/每行sum1；归一化矩阵需另名','A与归一化矩阵及w分别保存')
reg(22,'Q3',[39],'Table5-5 weights','权重来自特征向量','PRIMITIVE_RECOVERED','实为逐列归一化取行均值；审计首次误判已保留','按真实原语评价，不能称特征向量四舍五入','AHP_weight_primitive')
reg(23,'Q3',[39],'Table5-5 consistency','lambda6.61889,CI.0338,CR.0302','ARITHMETIC_CONFLICT','印刷矩阵lambda6.122463628,CI.024492726,CR.019752198(RI6=1.24)','重算仍过.1；不把原表错误夸大成必定不一致','AHP')
reg(24,'Q3',[39],'Tables5-6/7','GDP/pop2:1 → .0868/.1737','ENTITY_WEIGHT_REVERSAL','同一父权重不能将局部2:1变全局1:2','以indicator_id连接；按5-6条件修复非声称恢复最终地图','AHP_exposure')
reg(25,'Q3',[39,40,50],'future drivers/maps','2025–2035GDP/pop预测输入','UNREPRODUCED_FUTURE_SUPPORT','官方支持到2015；打印附录未给驱动预测链','情景/持久性与实际预测区分')
reg(26,'Q4',[49],'Table6-3','crop pair误写shrub；MSE皆高于','LABEL_AND_DIRECTION_DRIFT','表中353.752→330.730是耕地且MSE降低；R2.318→.362','按实体键生成表与正文，不能手工复制标签','Q4_table_relative_MSE_gains_percent')
reg(27,'Q4',[48,49],'heatmap/prose','pop-altcorr+.8说明高程低','SIGN_INTERPRETATION_CONFLICT','同样指标同方向编码时文字与正相关矛盾；底层编码未知','登记正向/反向编码，不改数值迁就文字')
reg(28,'Q4',[49,50],'land forecasting','五个独立变化率预测图','COMPOSITION_UNVERIFIED','没给联合份额界限、总量守恒、other类处理和未来driver链','独立回归仅候选；若转成份额，检验0..1及总量≤1/含other后=1')
reg(29,'Q4',[43,44,45,50],'usefulness','像地理分界线所以准确有用','EXTERNAL_UTILITY_NOT_ESTABLISHED','外观一致是合理性检查，不是独立用途评价','保留定性地图优点，另做决策用途验证')
dump('RESULT_REGISTRY.json',dict(source_sha256=access['source']['sha256'],policy='author claims preserved; local arithmetic/contract status separate from model accuracy',results=registry))
cards=[]
def card(q,p,task,target,baseline,author,alternatives,avoid,why,why_not,switch,six,module,errors,competition,limits):
    cards.append(dict(question=q,pdf_pages=p,task=task,target=target,baseline=baseline,author=author,alternatives=alternatives,not_recommended=avoid,why_select=why,why_not=why_not,switch_conditions=switch,six_hour_baseline=six,transferable_modules=module,error_modes=errors,reproduction_level='R2',reproduction_boundary=limits,method_competition=competition,skill_rule_action='Dev候选规则，记录来源；不进入Train检索，不追改冻结解答',validation='AUDIT_REPLAY.json local mechanisms; full author pipeline NOT_RUN',mini_transfer='题组S015/S016未完成；final groupMiniTransfer待题组结束，当前fixture非盲测'))
card('Q1',[6,18],'降水与土地时空变化描述','daily_mm→annual_total_mm；1990–2020降水/1990–2019土地，面积加权同一有效域',
 '冻结方案：共同支持域年累计/面积加权趋势与五类净变化；明确2020土地缺失',
 '逐日TIFF→递归平均→MK/Sen地图；五类覆盖度相对变化',
 ['带ties修正的MK+Sen描述趋势','OLS+块bootstrap置信区间；有季节性时季节分解'],
 ['直接把显著趋势当未来预测优胜','零值全删、不同掩膜总量相减、逐月均值等权'],
 '先保证量纲、时间轴、面积权重；作者MK/Sen可补描述但不改变原冻结结果',
 '作者聚合/年份/分类/打印数组存在冲突；不复制地图比例当真值',
 '仅在时间支持、mask、ties与自相关处理明确后采用MK；外推另需hindcast',
 ['0–1h数据日历/mask审计','1–3h年累计和面积总量','3–4h净变化/稳健斜率','4–5h局部数学校验','5–6h图及限制'],
 ['有tie的signed-pair统计量与exact小样本arbiter','效果方向和显著性分离','有效日数加权'],
 ['公式与代码分母不一致','效果阈值重叠','一维mask/二维栅格错配'],
 '冻结描述基线保留；作者稳健趋势为条件模块，不比较不同量纲全国均值',
 '只有Sen/MK打印代码；上游栅格生成缺失；未复现作者全国图')
card('Q2',[19,34],'地形气候与极端降水关系','作者长时段暴雨次数；冻结方案年度Rx1day，两者不可直接比较分数',
 '冻结年度Rx1day气候态；若改计数任务，先按有效日数估计常数/分区事件率',
 '线性回归、RF、SVM、XGB、AdaBoost，地形与平均温度→累计暴雨次数',
 ['带exposure offset的Poisson/负二项计数模型','GAM含地形-温度交互','浅树/RF作为同预算非线性候选'],
 ['按真实Y阈值选择预测分支','空间随机holdout支持未来或新区域外推','以importance作为因果机制'],
 '保持冻结验证选出的简单路线；新计数任务需新的独立评价合同',
 '作者XGB对RF表格MSE只降.441%，没有时空阻塞重复证据；与Rx1day分数不兼容',
 '统一target/cohort/offset/时空划分及训练预算，多块稳定实质增益且尾部误差不恶化',
 ['0–1h事件定义与有效日','1–2h空间对齐和循环坡向','2–3h常数/分区率','3–4hGAM或计数基线','4–5h阻塞验证','5–6h残差/数据限制'],
 ['同一heldout实体集合竞争','坡向sin/cos对齐','事件率分母随表输出'],
 ['shape匹配冒充地理对齐','NoData哨兵未清理','改cohort后直接比较R2'],
 'S014比冻结方案增加每日事件计数视角；不是用另一目标的高R2推翻冻结基线',
 'RF/XGB打印主循环可审计，但作者暴雨次数、坡度/温度中间栅格及模型产物缺失')
card('Q3',[34,42],'危险-暴露-脆弱性及未来情景','成灾标签缺失下的条件风险指数，不是校准灾害概率',
 '冻结Pcrit=K/[C(L)T]条件情景；持久性中心，历史rolling hindcast优于线性外推',
 'DEM排水网络+MK门控Sen预测+HEV/AHP/ArcGISWeightedSum',
 ['等权透明风险指数+权重敏感性','有观测时水文容量/损失模型','MK门控Sen参加同一滚动回测'],
 ['无灾情真值硬称临界阈值','HEV乘积与加权和互换','未来GDP/pop无来源'],
 '冻结方案有情景假设边界和持久性比较；不把作者未来地图当观测',
 '作者AHP表格及算子未闭合，driver缺链；复杂叠加不等于验证',
 '先统一目标、输入方向和HEV算子，未来驱动可执行；再做权重稳定性及独立损失验证',
 ['0–1h危险/暴露/损失分离','1–2h明确容量场景','2–3h持久性与滚动回测','3–4h透明指数','4–5h权重敏感性','5–6h地图和条件声明'],
 ['AHP矩阵/权重/一致性分别replay','indicator_id连接层级权重','记录聚合算子'],
 ['主特征向量名称掩盖实际列均值','GDP人口权重反转','显著趋势与可预测性混淆'],
 'S013/S014评价指数思想可对照；作者权重和阈值不直接拼入冻结容量方案',
 'Q3仅正文公式/表及GIS步骤，缺完整代码、专家判断原始记录、预测栅格')
card('Q4',[42,52],'土地变化特征结构与用途','冻结10维特征低维结构；作者五类变化率监督预测，任务侧重点不同',
 '冻结PCA+K5分区；报告重构与时间迁移ARI，外部用途尚未建立',
 '地理分界线解释+五类变化率RF/XGB+2025–2035预测地图',
 ['标准化特征+层次聚类/空间约束聚类','含other类的组成变化模型','持久性/零变化作为预测基线'],
 ['独立回归不检查份额可行性','预测地图看起来合理就称验证','crop/shrub标签手工复制'],
 '先满足紧凑描述任务；未来土地预测是额外目标，需不同验证',
 '作者未来驱动缺链、标签漂移、空间划分不清，不能拿训练后的地图证明用途',
 '预测任务须时空阻塞比较零变化和持久性；结构任务须外部用途或下游指标证明',
 ['0–1h有效域与组成界限','1–2h净变化+均值特征','2–3hPCA/简单分区','3–4h留出重构','4–5h时间稳定性','5–6h区域解释/用途限制'],
 ['entity-keyed表格与正文','预测份额界限和other闭合','用途与数值拟合分开'],
 ['变化率正负编码混淆','以相关性解释因果','标签与MSE方向漂移'],
 'S014提供更丰富地理叠图表达；不能替代冻结结构模型，也不证明Core净提升',
 '附录没有Q4训练数据构造/五模型预测链，故整体保持R2')
dump('QUESTION_CARDS.json',dict(paper='S014',split='dev',cards=cards))
gates=[
 ('输入输出接口','CONDITIONAL','必须有grid_id,time_support,mask,CRS,transform；shape相同不够'),
 ('变量定义','BLOCK_DIRECT_COMPOSITION','Rx1day、累计暴雨次数、降水年累计、灾害概率、指数互不等同；GDP密度非人均GDP'),
 ('数据分布','CONDITIONAL','随机空间holdout不匹配新区域/未来年份；采用共同空间块/滚动窗口'),
 ('数学假设','CONDITIONAL','MK独立性/ties、自相关，AHP互反性，HEV乘积/和需分别声明'),
 ('量纲','BLOCK_DIRECT_COMPOSITION','mm/day与mm/year、角度周期、GDP密度、归一化指标方向逐项核验'),
 ('训练执行阶段','BLOCK_UNSOURCED_FUTURE','未来GDP/pop不可从观测缺口静默补齐；参数仅训练/Dev选取'),
 ('评价指标','BLOCK_UNMATCHED_METRICS','同一target/cohort/单位/预算再比MAE/MSE/R2；图像合理性不是外部准确率')]
dump('METHOD_MAP_AND_COMPOSER.json',dict(status='PARTIAL_S013_S014_ONLY',case_group='2024-D',split='dev',not_final=True,remaining=['S015','S016'],selection=[dict(question=c['question'],selected=c['baseline'],author_candidate=c['author'],decision=c['method_competition']) for c in cards],seven_gates=[dict(gate=n,status=s,reason=r) for n,s,r in gates],composition_verdict='直接拼接被拒绝；只有修复接口并重新验证后才允许条件组合',mini_transfer='PENDING_COMPLETE_CASE_GROUP; local audit fixtures do not substitute'))
md('CODE_FORMULA_FIGURE_AUDIT.md','''# S014 代码、公式、图表审计

来源：D24104250063.pdf，62页；页码统一使用PDF页码（印刷页码少1）。全文与原PDF渲染62/62完成，打印Python附录53–62全部静态审计。视觉覆盖独立记录，不据此升级复现等级。原PDF含有效缩进，例如54页；抽取文本缩进丢失不作为作者语法错误证据。

Sen：读取1990–2019年中间栅格，逐像元全对斜率中位数；只接受所有年值大于0。MK：同样30年，signed-pair求S，方差除18但没有ties校正；sresult是一维，zc是二维，布尔赋值实际失败。正文12页分母30与代码不同，作者最终地图究竟来自哪版无法确认。

RF：read(1)丢弃地理元数据，按数组尺寸zoom(order=1)，flatten拼表，dropna，随机80/20，GridSearchCV5fold。XGB使用同样预处理，随机80/20和3foldCV。两者都是实际树回归主循环，不能说作者没有实现RF/XGB；但其原始输入是作者生成的暴雨次数、坡度、坡向和平均温度栅格，完整生成链不在打印附录中。坡向角直接线性插值会在359/1度处变成180度；有限NoData哨兵不会被dropna剔除。无crs/transform核验不能保证同一个地理点。

图4-19及附录sns.regplot展示的是拟合回归线，不能靠“点接近该线”证明接近y=x；两轴各取不同最大值也不保证视觉45度等于数值1:1。37页HEV乘积与39页WeightedSum是不同聚合模型；风险地图的输入归一化、权重、未来GDP/人口和输出版本未闭合。Q4未来变化率地图没有对应完整可执行链。

Table5-5权重可由列归一化取行均值恢复，这比“权重错误”的笼统结论更准确。但其lambda/CI/CR无法同时成立。局部复算与首轮审计错误完整保存在AUDIT_REPLAY_FIRST_FAIL.json和AUDIT_REPLAY.json。修复只针对可定位原语和合同，不声称作者整套结果已复现。

优势同样保留：日尺度事件计数、MK/Sen互补、多个回归候选、地理分界线的解释性叠图，都是值得保留的方案元素。主要瓶颈是定义、时间空间支持、验证方式和结果链，而非算法名称不够复杂。
''')
md('RULE_CANDIDATES_V140.md','''# S014 Dev 候选规则（尚未发布进稳定Core）

来源仅S014 Dev及本地数学/代码审计。Test比较内容未用于本增量。与v1.39数据合同规则去重后，拟扩展以下具体检查：

1. 扩展既有时间支持门禁：多级mean须保留有效样本数，mean-of-means不默认等于整体mean；年度累计、日均、面积加权分别命名。
2. 扩展既有实体/轴门禁：flatten后的统计量、布尔mask与输出栅格登记相同顺序及shape；矩阵计算、权重连接和输出表均保留indicator_id。
3. 扩展既有实际primitive审计：AHP主特征向量、几何均值、列归一化均值不得混称；A、w、lambda、CI、RI(n)、CR逐项重放，数值近似不能自动认作同一算法。
4. 扩展既有变量/单位门禁：循环变量重采样先处理周期；地理对齐登记crs/transform/extent/resolution/nodata，禁止只查数组大小。事件率同时登记有效暴露分母。
5. 扩展既有Result Registry：跨模型比较必须同target及heldout entity_id集合；真实Y条件只能用于事后诊断，不能成为未知Y时的模型路由规则；统计显著与预测增益分开。
6. 扩展既有组合门禁：分层权重按键传播，乘积与加权和保存不同operator_id；组成数据输出必须满足声明的总量及边界（五类不完备时加other或声明≤1）。

不另建同义规则或角色Skill。尚未修改稳定Core，也未把Dev卡片加入Train检索。候选代码为audit_replay.py中的局部函数；不是生产就绪地理分析库。审核这些扩展与现有长期规则的重叠后，再决定v1.40最终最小增量。

不得纳入通用规则的内容：作者60–90degree等具体阈值、AHP数值、地名风险判断和未来地图。不得因本地合同测试通过而声称clean blind Core gain。题组Mini Transfer在S015/S016完成后追加。
''')
md('S014_FINAL_REVIEW.md',f'''# S014 Dev 学习审计完成

S014《大数据驱动的地理综合问题》，2024-D / Dev。原PDF62页全文与视觉审查完成，打印附录53–62页静态审计完成，等级R2。源SHA256：{access['source']['sha256']}。

独立解答冻结SHA256：{access['independent_freeze_sha256']}。该解答先于S014暴露；本轮仅做Dev比较，没有追改冻结结果。复现等级不因局部合成数据试验上调。

审计已形成4份主要子问卡、29条Result Registry记录、S013/S014阶段方法竞争图和七门兼容性检查。直接拼接被拒绝；差异集中在目标定义、时空支持、量纲、未来驱动和评价总体。2024-D四篇题组尚未闭环，S015/S016仍待审查。

关键数值：7个不同值5040种排列确认MK方差44.333333，正文除30仅26.6；2x3栅格确认打印MK布尔轴错误；AHP印刷矩阵主特征值6.122463628、CI0.024492726、CR0.019752198，仍通过论文使用的0.1阈值。印刷权重来自列归一化均值，与主特征向量不同。GDP/人口局部与全局权重顺序反转。XGB相对RF的表格MSE改善约0.441%，不足以证明稳定实质优势。

第一轮本地审计28/29通过，失败是审计方假定AHP权重来自主特征向量；已定位其真实列均值原语，保留首次失败并复测。最终{replay['passed']}/{replay['total']}通过只指确定性局部合同/表格算术和错误检出，不代表作者整套模型准确、作者完整复现或Core能力提升。

四问的选择：Q1保留共同支持域累计/面积描述，MK/Sen作为条件模块；Q2冻结Rx1day基线与作者累计暴雨计数任务不直接比R2；Q3保留透明条件情景和持久性竞争，AHP作为待修复指数候选；Q4保留紧凑结构描述，作者未来土地预测需另建驱动与时空验证。

当前v1.40-work NOT SEALED；v1.39仍是正式稳定版。候选规则见RULE_CANDIDATES_V140.md，完整证据见RESULT_REGISTRY.json、QUESTION_CARDS.json、PAGE_AUDIT_LEDGER.json及AUDIT_REPLAY.json。系统保护与回归结果另见VALIDATION_S014.md。Clean blind Core-level gain=NOT_ESTABLISHED；No-Core/Previous-Core/New-Core=NOT_RUN。
''')
print('Built S014 review assets:',len(registry),'registry records;',len(cards),'question cards;62page ledger')
