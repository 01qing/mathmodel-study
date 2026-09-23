from pathlib import Path
import json, hashlib, re, subprocess, sys
ROOT=Path(__file__).resolve().parents[4]
CASE=ROOT/'learning_output/cases/2023-A-transfer'
def read(p):return p.read_text(encoding='utf-8-sig')
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')

old=read(CASE/'revision_v8/REFERENCE_SOLUTION.md')
base=old[old.index('## 摘要'):old.index('## 九、迁移结论与下一步论文对照')]
supp='''## 九、十篇学习后的模型取舍与质量要求

Q1继续使用有限求和固定点作解析基线，事件模型作机制对照。清分母多项式的根必须回代原式；p=0.5和1虽然可使某篇多项式为零，却不满足本题有限和闭合。二分和残差检验已经足以解该标量方程，没有证据支持增加复杂随机优化。

Q2保留16状态残余计数链。独立近似70.558464与联合链68.948748的差别来自建模假设，不能借修改退避计时让模拟去贴合近似。零退避合法，成功后窗口重置，双成功累计两个载荷。整个交换只占一段时间，与交付两个包并不冲突。

Q3可补充传输/失败状态解析模型：用f=Pc+(1−Pc)Pe闭合，窗口Wi=min(1024,Wmin*2^i)，归一化b00=1/Σ[f^i(Wi+3)/2]、τ=b00Σf^i；各驻留状态的不交叠概率按实际数据时长积分。完整分段和实现见第三篇q3_state_model.py及Q3_REVIEW.md。基础预测56.84642，对事件均值54.70608偏高3.91%；已测W16五组平均绝对相对偏差3.82%，W32两组14.74%。仅将其作为有适用范围的辅助解析，不替换事件主数值。其当前分段要求d/9非整数且小于Wmin、Ts/Tc不少于2d，边界需重新推导。

Q4除基础主情景，还采用两条邻接干扰边分别开关的条件化答案。相同5种子、0.5秒预热、5秒观测下：两边干扰110.831±0.201 Mbps，仅左边113.456±0.102，仅右边113.504±0.204，均不干扰117.085±0.159；中心分别11.928、14.689、14.658、17.843 Mbps。这里与主实验10秒口径不同，不改写主结果。四情景都显示中心较弱，尚未覆盖单向干扰和捕获效应。

每种事件分别列概率、时长、成功包数。概率必须属于[0,1]，互斥完备事件和为1；成功包数期望可以超过1，不能直接当概率使用。碰撞采用持久标记：只要本次数据帧曾有正长度干扰交叠，干扰者提前结束也不恢复成功；端点相接不碰撞。同一时刻事件共同处理，逐AP、逐包维护失败次数；所有能听到忙段的退避者冻结，交叠忙段取并集，恢复时遵守完整DIFS与时隙。

## 十、验证、误差与论文表达

本答案的数值来自已保存的本地模型实验，不把优秀论文报告值当作物理真值。冻结结果16场景、80次运行的包数与吞吐已核对。既有6类定向事件测试373项断言通过，另有四拓扑短轨迹29789项独立断言；这些数量对应各自既有检查，不是本轮新运行次数。成功载荷账本和发送时间并集独立核对，不用发送时间乘速率冒充成功比特数。

Q4基础各节点汇总失败率约2.7645%、18.0645%、2.7294%，系统仅4.6634%。总失败率与总吞吐都会掩盖中心节点劣势。Q3失败包含噪声和碰撞，不能与纯碰撞率或最终丢弃率混用。

对理论a和模拟均值b，吞吐相对误差定义为|a−b|/b；效率差定义为|a−b|/物理速率，报告百分比形式时应称效率的百分点差。例如某篇Q3的31.269与45.283 Mbps对应30.95%吞吐相对误差，而效率差仅3.07个百分点。RMSE须说明单位、是否归一化及样本集合，且同一集合下RMSE不小于|a−均值|。相关的时间窗口不增加独立种子数量。

经验系数先声明标定配置，再固定系数到独立配置验证；不在每一行重新拟合后报告预测准确。参数、公式、实际调用子函数和图表必须使用同一配置。正文与附录冲突保留记录，不静默修补成作者已验证的结果。

推荐图组各司其职：拓扑图与事件时序解释假设，状态/退避轨迹检验机制，参数曲线展示适用范围，逐节点图解释公平性，独立种子区间展示随机波动。当前已有图见第七节；作者原页视觉样式未逐图检验，不能声称完成版式复现。

## 复算与学习来源

主实验代码：[wlan.py](../code/wlan.py)、[run_experiment.py](../code/run_experiment.py)、[analytic.py](../code/analytic.py)；结果：[RESULTS.json](../results/RESULTS.json)。既有实验与所有局部检查按原参数、种子和观测时长区分，不必为阅读论文重复长仿真。

十篇逐问来源和采纳理由见[学习汇总](../LEARNING_SYNTHESIS_10_PAPERS.md)，逐篇原始路径及哈希见[PAPER_MARKDOWN_REGISTRY.json](../PAPER_MARKDOWN_REGISTRY.json)。第1–6篇详细历史验证保留在[上一版本](../revision_v8/REFERENCE_SOLUTION.md)和各篇目录；第7–10篇局部检查见[执行入口](../paper_learning/complete_remaining_checks.py)及各自CHECKS.json。

本题10/10篇可用全文文本学习完成，原作者完整程序复现0篇。本答案是同题学习后的条件性参考解答，不是新盲测，也未证明获奖率提升。正式Core仍v1.41.0，案例修订为v9；旧版和冻结首答保持原样。
'''
v9=CASE/'revision_v9'
write(v9/'REFERENCE_SOLUTION.md','# 2023年研赛A题：WLAN网络信道接入机制建模\n\n本地案例参考解答 v9 · 2026-09-22。已吸收十篇可用全文文本学习，整理统一正文；主模型与已保存实验数值未重估。正式Core v1.41.0。\n\n'+base+supp)
write(v9/'README.md','''# 2023-A 案例 v9

完整入口：[REFERENCE_SOLUTION.md](REFERENCE_SOLUTION.md)。本版整理统一正文，合并十篇学习所得模型取舍、事件检查及表达要求，不夹杂历次未完成状态。旧版v1–v8保留，正式Core仍v1.41.0。

学习记录：[十篇汇总](../LEARNING_SYNTHESIS_10_PAPERS.md)。作者程序完整复现0篇，本地实验与局部检查分别标注。本次没有重跑已有80次主实验，不宣称提升获奖率。
''')
state=json.loads(read(ROOT/'PROJECT_STATE.json'))
state['current_case'].update(status='TEN_FULL_TEXT_REVIEWS_WITH_SCOPED_CHECKS',reference_solution='learning_output/cases/2023-A-transfer/revision_v9/REFERENCE_SOLUTION.md',next_action='Select a local new problem with unseen same-problem answers; inspect prompt/data only, produce and freeze a full solution before paper comparison. LOCAL ONLY; no PDF parsing.',same_problem_solution_exposure='After first-answer freeze: all ten available-text papers reviewed; not a fresh blind test',papers_full_text_reviewed=10,papers_end_to_end_reproduced=0,partial_paper_reviews=[],synthesis='learning_output/cases/2023-A-transfer/LEARNING_SYNTHESIS_10_PAPERS.md')
dump(ROOT/'PROJECT_STATE.json',state)
reg=json.loads(read(CASE/'PAPER_MARKDOWN_REGISTRY.json'))
pages={'A23103360079':77,'A23103840031':55,'A23104860166':68,'A23105330383':63}
for p in reg['papers']:
 if p['paper_id'] in pages:
  pid=p['paper_id'];p.update(status='FULL_MARKDOWN_REVIEW_PARTIAL_NUMERICAL_CHECKS',reading_scope=f'All {pages[pid]} available converted pages and appendix text. Scalar reconstructions and isolated event/operator checks; no image-pixel inspection or full author-program execution.',review=f'paper_learning/{pid}/REVIEW.md')
dump(CASE/'PAPER_MARKDOWN_REGISTRY.json',reg)
progress='''# 本地学习进度：2023-A已收尾

2026-09-22。10/10篇、共660转换页的可用全文及附录文本学习完成。原作者完整程序复现0篇；公式缺失和图像未核验处保留限制。最新完整参考答案为revision_v9/REFERENCE_SOLUTION.md，十篇方法汇总为LEARNING_SYNTHESIS_10_PAPERS.md。正式Core仍v1.41.0，45篇基线和32/7/6划分不变。

本轮完成A23103360079、A23103840031、A23104860166、A23105330383逐问评审、标量与隔离机制检查，并写入本地知识卡。已有前六篇检查和80次主实验复用，不重复训练。这里是方法库学习，不是模型权重更新或获奖率提升证明。

下一步选择本地未读同题答案的新题，只看题面和附件，独立完成推导、代码、结果、验证与全文参考解答，冻结后再与优秀论文对照。先登记既有暴露，不能将已读答案包装成盲测。无需用户先提供自己的解答；若必要输入仅有PDF，说明缺失内容，由用户转换Markdown。

仅本地，不处理GitHub，不解析PDF。保留原始论文、41项冻结文件和历次解答。不要再次把本组十篇标为未读或重启逐篇学习。
'''
write(CASE/'PAPER_REVIEW_PROGRESS.md',progress)
write(ROOT/'learning_output/context/next_learning.md',progress)
ls=json.loads(read(ROOT/'learning_output/context/learning_state.json'))
ls['current_focus'].update(year=2023,problem_id='A',mode='review',session_id='20260922-2023A-ten-paper-completion')
ls['next_actions']=[state['current_case']['next_action'],'Preserve 2023-A frozen first answer and all source Markdown; use v9 and ten-paper synthesis; no new Core release.']
ls['local_delivery_20260922']=dict(case='2023-A-transfer',status='TEN_FULL_TEXT_REVIEWS_WITH_SCOPED_CHECKS',reference_solution=state['current_case']['reference_solution'],papers_full_text_reviewed=10,author_full_program_reproductions=0,not_new_release=True)
dump(ROOT/'learning_output/context/learning_state.json',ls)
notice='> 最新状态（2026-09-22）：2023-A的10/10篇可用全文文本已学完，完整参考答案为learning_output/cases/2023-A-transfer/revision_v9/REFERENCE_SOLUTION.md，汇总为同目录LEARNING_SYNTHESIS_10_PAPERS.md。下一步做新题先答后对照的迁移检验。作者完整程序复现0篇，正式Core v1.41.0不变。只在本地，不处理GitHub、不解析PDF。下方旧进度为历史记录，以PROJECT_STATE.json为准。\n\n'
for name in ['START_HERE.md','HANDOFF_NEXT_CHAT.md','NEW_CHAT_PROMPT.md']:
 p=ROOT/name
 if not read(p).startswith(notice):write(p,notice+read(p))

freeze=json.loads(read(CASE/'FIRST_ANSWER_FREEZE.json'))
bad=[n for n,h in freeze['files'].items() if hashlib.sha256((CASE/n).read_bytes()).hexdigest()!=h]
source_bad=[]
for p in reg['papers']:
 for kind in ['markdown','raw_layout']:
  if hashlib.sha256((ROOT/p[kind+'_repo_path']).read_bytes()).hexdigest()!=p[kind+'_sha256']:source_bad.append(p['paper_id']+':'+kind)
assert not bad and not source_bad
assert len(reg['papers'])==10 and all(p['status']=='FULL_MARKDOWN_REVIEW_PARTIAL_NUMERICAL_CHECKS' for p in reg['papers'])
for p in reg['papers']:assert (CASE/p['review']).is_file()
for pid in pages:json.loads(read(CASE/'paper_learning'/pid/'CHECKS.json'))
links_bad=[]
for p in [v9/'REFERENCE_SOLUTION.md',CASE/'LEARNING_SYNTHESIS_10_PAPERS.md']:
 for link in re.findall(r'\]\(([^)]+)\)',read(p)):
  if not link.startswith(('http','#')) and not (p.parent/link).exists():links_bad.append(str(p)+':'+link)
assert not links_bad,links_bad
run=subprocess.run([sys.executable,str(ROOT/'.agents/skills/graduate-mathmodel-learning/scripts/validate_learning_workspace.py')],cwd=ROOT,capture_output=True,text=True)
assert run.returncode==0,run.stdout+run.stderr
result=dict(status='PASS',frozen_files_checked=len(freeze['files']),frozen_mismatches=bad,source_text_files_checked=20,source_mismatches=source_bad,review_files=10,new_scoped_check_files=4,reference_links_broken=links_bad,workspace_validator=run.stdout.strip(),papers_full_text_reviewed=10,author_full_program_reproductions=0,core_version='1.41.0',case_version='v9')
dump(CASE/'BATCH_REVIEW_VALIDATION.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
