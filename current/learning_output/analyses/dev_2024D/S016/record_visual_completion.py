"""Record the pages actually viewed in the session; rendering alone is not review."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
P=Path(__file__).resolve().parent
W=P.parents[3]
prior=[22,29,42,87,104,112]
batches=[[13,17,21,25],[26,32,33,34],[35,46,48,50],[47,51,52,54],
 [55,58,60,61],[65,66,67,73],[74,76,77,78],[79,80,81,82],
 [1,2,3,4],[5,6,7,8],[9,10,11,12],[14,15,16,18],[19,20,23,24],
 [27,28,30,31],[36,37,38,39],[40,41,43,44],[45,49,53,56],
 [57,59,62,63],[64,68,69,70],[71,72,75,83],[84,85,86,88],
 [89,90,91,92],[93,94,95,96],[97,98,99,100],[101,102,103,105],
 [106,107,108,109],[110,111,113,114]]
seen=sorted(set(prior+[p for batch in batches for p in batch]))
assert seen==list(range(1,115))
notes={
 1:'封面身份核验。',2:'摘要Q1方法与损失/显著性主张。',3:'摘要Q2–Q4与风险40%主张，来源未闭合。',
 5:'六类数据说明，西经/南纬标记不当。',6:'分辨率1km与0.1km文字冲突。',
 13:'季节图色标范围不同。',14:'异常值处理与箱线图，年与日尺度待核对。',
 15:'Eq3.1日均定义与年降水名称不一致。',16:'Eq3.2 n/(n−1)系数；年累积文字与公式不一致。',
 17:'历史拟合图不等于独立验证。',18:'ARIMA文字切分边界2015重复。',19:'图横轴2001–2020与标题1990–2020。',
 20:'LSTM概念图及公式不代表完整训练链。',21:'训练loss与平滑的历史预测曲线。',
 22:'表3.3预测和真值逐项相同；与p87冲突（此前已看）。',
 23:'均值公式显示异常，缺少对应统计定义。',24:'雨量图掩膜图例为无植被覆盖。',25:'Moran曲线及CV公式。',
 26:'CV图与滑动平均后MK，相关性边界。',27:'显著性点图及土地动态度公式。',28:'Q/LUD/LUC公式和分母。',
 29:'表3.4数值及守恒矛盾（此前已看）。',30:'土地颜色图缺逐幅年份标签。',31:'Sen趋势与NPP来源/单位。',
 32:'NPP图轴gC，文字Hz；横轴2001–2020。',33:'六区NPP分段趋势，标题跨度不一致。',34:'NPP图例和2001–2020分段。',
 35:'年雨量增减叙述冲突，694mm与附录不同源。',38:'stacking框图缺执行链。',40:'MK标签配Sen斜率。',41:'Sen标签配MK符号和；变量身份漂移。',
 42:'联合上尾式却用下尾CDF（此前已看）。',43:'偏导标签与参数合同不一致。',44:'上层气象驱动不在列明数据源中。',
 45:'min_length伪代码，无空间键连接证据。',46:'RF报告低R²，未确认独立留出。',47:'高值预测压低和残差长尾；负温剔除风险。',
 48:'OLS输出R².078、n339591、DW.131，标准化系数。',49:'海拔负柱图被文字解释为正；直方图不是效应图。',50:'系数表负号与前页叙述。',
 51:'预测轴解释反向，全国图无数值色标。',52:'相关/重现期图无数值色标。',53:'OLS文字与logit公式并置；坡向sin/cos可取但要重建验证。',
 54:'TIN和气象图华北局部域。',55:'局部极端频率图和作者明确低解释力限制。',
 57:'LSTM/logistic框图的输入标签与p56/59文字对调；AHP灾害真值缺失。',58:'区域独立假设忽略上下游作用。',59:'RAI单位/持续时间；独立logistic组成不闭合。',
 60:'脆弱性地图不是已校准灾害概率。',61:'11年未来地图不构成独立回测。',62:'RF标题下OLS实际流程。',
 63:'OLS n501301,R².134,DW.140。',64:'真实行/预测列混淆矩阵9733,1944,2177,5137；下图是特征直方图非回归系数。',
 65:'七系数图与未来降水独立色标。',66:'2034/2035降水不同色标；温度图有一致色标。',67:'类别图被解释成覆盖面积；DW限制明确。',
 70:'降水图两图层尺度/日期未统一说明。',71:'温度图例含2005，非全期汇总证明。',72:'城市用地转移结论超出五类输出编码。',
 73:'符号转移矩阵与计数文字，不是已归一化实数矩阵。',74:'公式最后项被页边裁切，不能猜测标签回流。',
 75:'LUSC指标概念及作者参数设定。',76:'AUC1/.75仅文字，缺ROC/逐样本证据。',77:'Gain缺父子差；70/15/15无键清单。',
 78:'SHAP存在NDVI及QW名称映射疑点。',79:'Force输出4.67；PD红色正贡献。',80:'Decision输出约1–7被称概率，输出空间不明。',
 81:'Correlation图被称协方差，相关不能识别转移。',82:'政策效用主张无识别链。',83:'结论不补缺失模型证据。',84:'八项参考文献，NPP外部硕士论文。',
 85:'表7.6年份均值/SD/max非海拔系数；1990–2018。',86:'2019–2020续表及2021–2025预测数值。',87:'表7.8与p22不同源（此前已看）。',
 88:'loss1–30仅训练数值。',89:'loss31–62。',90:'loss63–94。',91:'loss95–100，最终.04663350060582161。',
 92:'pandas默认header的CSV导出。',93:'C++逐行stod，无header跳过。',94:'近零背景及后序优先argmax。',95:'1–5类别以空格输出，0背景。',
 96:'经纬度平面多边形面积乘统一常数。',97:'Totalarea4186与无标题跳过读取器。',98:'Q符号/倍数与正文不同；subtractpath只保留正差。',
 99:'空vector和forest缺定义；9年端点却用10年。',100:'K三段调用和LC文件1990–1999。',101:'LC1990/1999、2000/2009，标签拼写错误。',
 102:'LC后两期文件，不能与LUD误用文件混同。',103:'LC2010/2019正确端点但Q按数组索引。',104:'LUD后两期同读2010/2009（此前已看）。',
 105:'forest/grass LUD两期重复2010/2009。',106:'shrub/wet LUD重复；wet中期分母竟[0]。',
 107:'crop/forest LUC重复2010/2009。',108:'grass/shrub/wet LUC同一时点错误。',109:'wet LUC末期同错误；main结束。',
 110:'PIL RGB图，无CRS/transform写入。',111:'MK符号和，标题Sen；alpha外部未定义、无ties方差修正。',
 112:'channel/label/user_id归因类，不是高斯偏导（此前已看）。',113:'OR推AP/PAF与groupby计数。',114:'渠道配对及RR/RD/OR/AP/PAF调用，无气象运行链。'}
ledger={'paper_id':'S016','source_sha256':hashlib.sha256((P/'source.pdf').read_bytes()).hexdigest(),
        'visual_review_count':len(seen),'page_count':114,'text_read_count':114,
        'review_method':'Actual original PDF rendered pages viewed using view_image; not OCR-only or file existence.',
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'VISUAL_AND_STATIC_AUDIT_ONLY','reproduction_level':'R2','pages':[]}
for p in seen:
    png=P/'visual'/f'p{p:03d}.png'
    ledger['pages'].append({'physical_page':p,'visual_reviewed':True,
      'evidence_origin':'prior_session_record' if p in prior else 'current_session_view_image',
      'png_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),
      'note':notes.get(p,'全文段落/变量与方法说明完成原页核对；具体论证见PARTIAL_REVIEW和QUESTION_COMPETITION。')})
(P/'PAGE_AUDIT_LEDGER.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
status_path=W/'WORK_STATUS_V141.json'
status=json.loads(status_path.read_text(encoding='utf-8-sig'))
status['S016']['visual_read']=seen
status['S016']['status']='FULL_TEXT_AND_VISUAL_COMPLETE_QUESTION_COMPETITION_PENDING'
status['S016']['reproduction_level']='R2'
status['S016']['visual_followup_tests']={'passed':11,'total':11,'scope':'LOCAL_ARITHMETIC_AND_SYNTHETIC_MECHANISMS_ONLY'}
status_path.write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'visual_count':len(seen),'missing':sorted(set(range(1,115))-set(seen))}))
