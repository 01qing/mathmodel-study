from pathlib import Path
import json
H=Path(__file__).resolve().parent;O=H/'results'
r=json.loads((O/'RESULT_REGISTRY.json').read_text(encoding='utf-8'));a=json.loads((O/'feature_audit.json').read_text(encoding='utf-8'));q=r['claims'];v=json.loads((O/'INDEPENDENT_VALIDATION.json').read_text(encoding='utf-8'))
def write(n,t):(H/n).write_text(t,encoding='utf-8')
write('DEV_2024D_DATA_AUDIT.md',f'''# 2024-D 数据审计

来源仅限官方题面及六组附件。输入SHA见original-inputs/RAW_INPUT_MANIFEST.json。六组所选解压成功；不是全库所有年份全部学习。DEM使用Geo TIFF；气温1990–2018共10592日；降水1990–2022逐日；土地覆盖分析1990–2019，人口/GDP分析1990/2000/2010/2015四个锚点。

共同0.5°分析网格保留{a['common_support']['cells']}格，整格面积约{a['common_support']['area_km2']:.0f} km²。这是覆盖至少50%降水有效区并具有地形/土地数据的分析支持域，不能当精确中国行政面积。边界整格计面积会造成偏差；未包含有效观测的地区不以零值代替。

DEM元数据nodata缺失，已剔除{a['dem']['masked_sentinel_count']}个-32768像元；有效高度0–8848m。实际CRS为Krasovsky，与题面WGS84描述不符，按文件CRS转换，未建立精密大地基准变换。地形起伏指标是格内高程标准差，不是坡度或汇流面积。

降水missing_value为字符串-99.9，库警告不能自动mask；已显式按负值屏蔽。先按经纬网格球面重叠聚合每日降水，再计算年总量和Rx1day，避免“先求局部最大再平均”混淆。Rx5day窗口仅在同一日历年内，未用于核心结论。

气温先在原生网格汇总全年，要求至少95%日有效，再投影平均。年平均温度只能支持事后关联建模。土地五类比例总和最大{a['land']['sum_max']:.9f}，超过1.001的格时记录为0；残余类型未知，未当不透水面积。2020土地覆盖无观测，不补造。

人口/GDP以源像元中心归属求和，在共同矩形范围内守恒；最大相对误差{max(c['relative_conservation_error'] for c in a['socio']['checks']):.3g}。该方法有约1km边界归属近似。GDP价格基期未核实，不把名义增速等同于适应能力改善。未来情景固定2015社会经济。

独立重叠聚合核验在三个内部网格对365日1990原始降水直接逐交叠求和，另见INDEPENDENT_VALIDATION.json。未证明全域/全部变量的外部数据真实性。
''')
models='\n'.join(f"- {x['model']}：开发MAE={x['validation_MAE_mm']:.4f}mm，最终留出MAE={x['final_MAE_mm']:.4f}mm；空间胜出{x['spatial_wins']}/5。" for x in q['Q2']['models'])
write('DEV_2024D_MODEL_COMPETITION.md',f'''# 独立 Candidate Model Competition

作者方案：PROTECTED_NOT_READ。四问都未使用优秀论文答案；不能为了填写作者方案字段打开Dev。

Q1：基线为面积加权均值与五类比例时间序列；推荐增加降水空间趋势/CV、土地净变化/组成距离，控制为每变量三幅子图。替代为分位数分区或变点检测；当前不推荐复杂时空网络，因为任务是描述，且没有验证收益。需要局部极端分布时切换分位数；新增观测后才补2020土地数据。

Q2：最简单基线是每格训练期Rx1气候均值；加性样条Ridge提供地理位置、地形、气温的平滑解释；交互候选加入地形×气温乘积；主要非线性替代是浅层梯度提升。参数在首次拟合前固定。空间与时间验证见预注册文件。最终主线选择 **{q['Q2']['selected']}**。
{models}
复杂候选须开发MAE至少改善5%，且5个空间折至少4折改善才可进入推荐。未满足时保留简单基线；预测提升不等于因果地形作用。深度时空网络不推荐，缺独立增益证据且预算风险高。有独立观测、同条件稳定改善时再升级。

Q3：稳妥基线是近期极端降水气候均值+固定土地/社会经济的压力地图。推荐把趋势/无趋势、土地变化/不变、径流系数和容量组合成透明情景，并报告排名稳定性。替代是含真实灾害标签的空间逻辑模型，或含河网/排水/土壤参数的水文模型；现有数据无法校准，暂不选。禁止训练以自造风险分数为标签的分类器后宣称灾害准确率。真实灾害记录及排水条件补足时才能切换。当前临界条件是明确假设的机制条件，不是已验证灾害阈值。

Q4：基线为全域单一组成原型，推荐开发空间块选定的{q['Q4']['selected_k']}类组成/变化原型；两维PCA为低维连续替代。K=2/3/4/5使用相同输入与划分比较；不推荐任意划线和只凭轮廓系数命名地理规律。需要连通的管理分区时再增加空间连续约束并重做外部有用性验证；当前聚类可不连续。

## Method Composer 七门
1. 输入输出：栅格均转共同网格并保留mask；Q2的预测器没有伪装为Q3灾害发生器，Q3直接使用观测Rx1历史统计。
2. 变量定义：Rx1是格面日均降水的年最大，不是点暴雨；比例不是土地转移；高程起伏不是水文坡度。
3. 数据分布：训练/开发/最终年份和空间块分开；未来趋势超分布风险明确。
4. 数学假设：Q2为关联，Q3为假设压力模型；不把两者组合成因果证明。
5. 量纲：降水和容量均mm/day，系数/地形乘子/排名指数无量纲；人口和GDP先按总量聚合。
6. 阶段：所有拟合变换在训练块内；未来情景不作为已观测训练目标；核心规则未改。
7. 指标：Q2 MAE衡量Rx1预测，Q4 RMSE衡量组成重建，Q3稳定性不等于预测准确率；不得跨指标相加选“冠军”。
''')
back='\n'.join(f"- 截至{x['fit_end']}拟合、验证{x['target_years']}：持续性MAE {x['persistence_MAE_mm']:.3f}mm；线性趋势 {x['linear_MAE_mm']:.3f}mm。" for x in q['Q3']['backtests'])
write('DEV_2024D_INDEPENDENT_SOLUTION.md',f'''# 2024-D 独立解答

本答案由agent按冻结MathModel-Core v1.38规则，仅基于官方问题/附件独立形成；不是人类正式参赛稿。计算代码、假设、参数、结果和限制全部保留。冻结状态以同目录freeze manifest为准。

## Q1 时空演化
1990–2020共同分析支持域的平均年降水为{q['Q1']['mean_annual_precip_1990_2020_mm']:.3f}mm；面积加权全国序列OLS趋势为{q['Q1']['national_precip_trend_mm_decade']:.3f}mm/十年。描述性趋势不附因果解释，也未宣称统计显著。
土地覆盖1990–2019净变化（百分点）：{json.dumps(q['Q1']['land_net_percentage_points_1990_2019'],ensure_ascii=False)}。
见figures/Q1_precipitation.png、Q1_landcover.png及两份Q1 CSV。每个变量三幅子图，分别表达时间、空间和离散/组成变化。由于2020土地数据缺失，这一年的观测要求明确未满足，不使用未来外推填充实际观测。

## Q2 地形–气候相互作用
令Y为每个0.5°格每年的Rx1day，候选特征为经纬度、高程、起伏度、年均温与年份。加性样条回归以平方误差和L2正则求解；交互模型增加高程×温度、起伏×温度，梯度提升作为非线性替代。训练1990–2005，开发2006–2010，最终2011–2018，另做五个5°空间块验证。
{models}
根据预先固定门槛选择{q['Q2']['selected']}。这些对照只评价预测关联，不能证明地形或温度的因果贡献；降水产品本身已使用PRISM地形校正。年均温是事后可见变量，所以这不是提前极端天气预报。若复杂路线未胜出，应明确保留失败而不是改门槛。

## Q3 临界条件及2025–2035情景地图
采用条件式 `Pcrit=K/[C(L)T]`：P与容量K以mm/day计，C为土地组成加权系数，T为地形修正假设。K取25/50/100，C和T详见RESULT_REGISTRY与源码。它展示同等降水下条件差异，不是已校准成灾临界值；缺灾害标签、土壤、河网、设施和损失数据，此缺口无法通过更复杂算法补齐。
历史五年外推对照：
{back}
中心气候路线选{q['Q3']['central_climate']}。2025/2030/2035各36组合，包含两种气候路线、两种土地路线、三组系数和三种容量。未来温度未外推，人口/GDP固定2015。地形起伏和低高程、人口密度、GDP/人的百分位仅为相对代理。
地图见figures/Q3_scenario_maps.png；高排名格的经纬度与稳定性见results/Q3_top_cells.csv。颜色代表相对情景压力或位于最高十分位的情景比例，不能读作灾害概率。容量K是全国统一乘数，改变绝对压力但不改变同情景排名，因此36组合不等于36个独立排名实验。另有系数与地形假设未完全覆盖，不能夸称全面鲁棒。

## Q4 土地变化结构综合
以五类1990–2010均值和五类净变化组成10维分数向量；在空间训练块拟合KMeans和PCA。开发误差选择最小、且在最优误差10%以内的K，最终为{q['Q4']['selected_k']}；最终测试块不参与选择。两维PCA解释方差比例{q['Q4']['PCA2_explained_variance']}，测试重建RMSE={q['Q4']['PCA2_test_RMSE_fraction']:.5f}。
时间窗移至1999–2019后，相同原型分类的ARI={q['Q4']['window_shift_ARI']:.4f}。这衡量表征随时间变化的稳定性，不能把真实变化全称为模型失稳。地图、各K误差和原型保存在Q4图、Registry与npz中。准确性证据限于空间留出重建；有用性是数据压缩和提供可解释组成原型，尚无外部政策收益验证，聚类也不保证空间连通。

## 证据等级与未解决事项
当前属于官方数据上的可执行独立基线与有限验证，未进行优秀论文复现；不新增或拔高R0–R7作者复现等级，更不是R7。Clean blind Core-level gain=NOT_ESTABLISHED，No-Core/Previous-Core/New-Core=NOT_RUN。历史pristine未完全核实，本轮未读Dev/Test答案。
回归/守恒/重放通过只支持对应计算合同。未建立：校准灾害阈值、真实未来灾害预测准确性、因果地形效应、完整行政边界精度、Core能力增益。保留这些边界后冻结本独立答案，供未来授权后的Dev比较，不以不足为由提前看优秀论文。
''')
write('VALIDATION_V139.md',f'''# v1.39 independent-solution validation

Numerical checks: {sum(c['pass'] for c in v['checks'])}/{len(v['checks'])}, scopes in results/INDEPENDENT_VALIDATION.json. Frozen original Core bytes unchanged. No full historical regression rerun claimed. Visual QA and deterministic replay are recorded separately in final manifest evidence.

Failure history: RAR/CRLF parsing, Unicode NetCDF lookup, initial unmatched parenthesis, missing pyproj dependency; each diagnosis/repair retained in handoff history and protocol note. Core's prior Mini Transfer failures are unchanged. This Dev run does not replace those records or declare a new transfer PASS.

No-Core/Previous-Core/New-Core NOT_RUN; disaster probability NOT_ESTABLISHED; historical pristine UNVERIFIED. No protected excellent-paper access in this session.
''')
write('PROGRESS_V139.md','''# v1.39 / 2024-D independent solution milestone

The four-question independent computation and evidence-bounded answer are complete. Frozen Core remains v1.38.0; no generic Core rules updated. The independent solution is sealed only when DEV_2024D_FREEZE_MANIFEST.json declares INDEPENDENT_SOLUTION_FROZEN and its hashes verify. This is not a claim that Dev comparison or v1.39 Core training is complete. STOP before S013; obtain the next user instruction after reporting the freeze.
''')
print('reports written')
