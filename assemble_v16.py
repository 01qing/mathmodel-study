from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).parent; D=W/'v1.6'; S=D/'.agents/skills/graduate-mathmodel-learning'; OLD=W/'v1.5-original'
def save(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def append(p,text):p.write_text(p.read_text(encoding='utf-8')+'\n'+text,encoding='utf-8')
m=json.loads((W/'evidence/manifest.json').read_text(encoding='utf-8'))
by={x['id']:x for x in m}
papers=[]
for x in m:
    if int(x['id'][1:])>45:continue
    pages={'S039':[1],'S040':[1,37,38],'S041':[1]}.get(x['id'],[])
    papers.append({'source_id':x['id'],'path':x['path'],'sha256':x['sha256'],'page_count':x['pages'],
                   'reviewed_pages':pages,'review_status':'partial' if pages else 'not_reviewed',
                   'review_evidence':'references/2025-E-evidence-lessons.md' if pages else None})
save(S/'assets/catalog/local_papers_2024_2025.json',{'schema_version':'1.6','materialized_count':len(papers),'papers':papers,
     'note':'Only explicitly registered selected E pages count as reviewed here; earlier screening excerpts are not promoted to full review.'})
manifest=json.loads((S/'templates/case_manifest.json').read_text(encoding='utf-8'))
problem=next(Path('D:/BaiduNetdiskDownload/2025年中国研究生数学建模竞赛赛题').rglob('*.docx'))
manifest.update({'case_id':'gmcm-2025-E','year':2025,'problem_id':'E','canonical_working_title':'高速列车轴承智能故障诊断问题',
 'title_status':'confirmed','problem_assets':[{'path':str(problem),'sha256':hashlib.sha256(problem.read_bytes()).hexdigest(),'role':'local_problem_statement'}],
 'excellent_papers':[p for p in papers if p['source_id'] in ['S039','S040','S041']],
 'status':'PARTIAL_REFERENCE_STUDY','fresh_blind_eligible':False,'solution_exposure_before_matrix':True,
 'raw_signal_reproduction':'NOT_RUN','target_accuracy':'UNKNOWN','method_family_expectations':{'Q1':'signal features','Q2':'grouped source classification','Q3':'unsupervised adaptation','Q4':'interpretability'}})
save(S/'assets/cases/2025_E_case_manifest.json',manifest)
findings=[
 ('g-template','S048','问题2随机森林代码.py','limitation','partially_verified','medium','代码使用例子数据.csv和X1/X2，尚非完整赛题数据流'),
 ('g2-group','S051','main8.py:SourceBearingDS.__init__','strength','verified','info','先按原文件划分，保留优点；仍需类别与副本检查'),
 ('g2-fs','S051','main8.py:SourceBearingDS.__getitem__','implementation','verified','critical','48kHz与lower()大小写不一致，回退分支误判采样率；局部表达式已复现'),
 ('x-pca','S054','solve1.ipynb:MinMaxScaler/PCA before train_test_split','leakage','verified','critical','PCA分支在全体特征拟合后划分；静态数据流确认，非全部模型分支结论'),
 ('x-fallback','S054','solve3.ipynb:USED_PROXY_TARGET','scope','verified','high','目标缺失时源测试信号和生成特征只能标为代理实验'),
 ('x-maha','S054','solve4.ipynb:maha_score','implementation','verified','high','距离二次型下标错误，局部原函数产生负平方距离'),
 ('raw-missing','S054','source raw MAT to features','evidence_gap','unresolved','high','未从原始MAT重做特征链路，派生表实验不等于完整复现')]
audit={'schema_version':'1.1','case_id':'gmcm-2025-E','audit_id':'local-2025-E-v16','repository':'user-provided-local-reference-archives',
 'audited_files':[{'source_id':sid,'archive':by[sid]['path'],'archive_sha256':by[sid]['sha256'],'member_or_location':loc} for _,sid,loc,*_ in findings],
 'findings':[{'id':i,'source_id':sid,'location':loc,'finding_type':typ,'status':status,'severity':sev,'observation':msg,
              'verification_scope':'Specific observation only; no whole-pipeline correctness claim'} for i,sid,loc,typ,status,sev,msg in findings],
 'summary':{'full_reproduction':False,'raw_signal_reproduction':'NOT_RUN','evidence':'assets/cases/2025_E_regression_results.json'}}
save(S/'assets/cases/2025_E_external_code_audit.json',audit)
review=json.loads((S/'templates/paper_review.json').read_text(encoding='utf-8'))
review.update({'review_id':'2025-E-S040-partial','source_id':'S040','problem_id':'E','review_scope':'PDF pages 1,37,38 only',
 'questions':[{'question_id':'Q3','author_claim':'平均置信度0.992','status':'contradicted','observation':'表6-2的16个值算术均值0.9246875',
               'caveat':'若另有权重或运行版本需补充说明；不能将置信度当准确率','pages':[37,38]}],
 'overall_transferable_lessons':['从原结果表重新计算正文汇总数字'], 'do_not_copy_blindly':['未经解释的正文均值','无真值目标准确率']})
save(S/'assets/cases/2025_E_paper_review_partial.json',review)
card=json.loads((S/'templates/method_card.json').read_text(encoding='utf-8'))
card.update({'method_id':'grouped-signal-validation','name':'以原始采集文件为单位验证信号模型',
 'core_idea':'同文件的窗口和通道继承组，训练折内拟合预处理，按文件汇总预测',
 'problem_families':['signal classification'],'key_assumptions':['group identifies independent acquisition; duplicate copies mapped to same group'],
 'data_requirements':['raw-file identity','labels','window/channel provenance'],'suitable_for':['多窗口设备诊断'],
 'not_suitable_for':['缺少来源映射时直接宣称已隔离'], 'baseline_against':['random row split used only as diagnostic'],
 'alternatives':['leave-device-out','leave-condition-out'],'switch_conditions':['目标推广到新设备或工况时改用对应留组验证'],
 'validation':['组交集为空','每折类别覆盖','文件级Macro-F1与少数类召回'],
 'common_failures':['切窗后随机拆分','全体PCA后拆分'],'sources':['gmcm-2025-E:S054'],
 'learning_level':'unseen','evidence_status':'partially_verified','note':'Agent资料库新增不自动升级用户掌握度'})
save(S/'assets/cases/2025_E_method_card.json',card)
for a,b in [('feature_benchmark.json','2025_E_feature_benchmark.json'),('regression_results.json','2025_E_regression_results.json')]:
    shutil.copy2(W/'evidence'/a,S/'assets/cases'/b)
shutil.copy2(Path('C:/Users/lingyun/.codex/skills/mathmodel-evidence/scripts/compare_features.py'),S/'scripts/benchmark_2025_E_reference_features.py')
shutil.copy2(Path('C:/Users/lingyun/.codex/skills/mathmodel-evidence/references/source-lessons.md'),S/'references/2025-E-evidence-lessons.md')
text=(S/'references/2025-E-evidence-lessons.md').read_text(encoding='utf-8')
text=text.replace('没有旧v1.5实际文件，未合并旧实现。','v1.6已取得旧v1.5并以其为基底合并本记录。')
text=text.replace('`compare_features.py`','`benchmark_2025_E_reference_features.py`')
(S/'references/2025-E-evidence-lessons.md').write_text(text,encoding='utf-8')
append(S/'references/candidate-model-competition.md','''
## v1.6：把质疑转成行动
每轮选1–3个能改变决策的问题，记录question、evidence、test、result、decision、unresolved。检验未运行就写NOT_RUN。每项质疑应触发数据核验、同边界模型对照、反例或消融，不靠反复解释提升置信度。无新证据时停止循环并保留限制。
训练变换在训练折内拟合；分组/工况边界先于模型选择。参考派生表实验不升级为原始数据复现。CV折差的1.96×SE只能作粗略诊断，不能称严格置信区间或证明实践等价；小差异可优先简单模型并说明不确定性。
''')
append(S/'references/evidence-and-verification.md','''
## v1.6证据范围
verified须附核验范围：原表达式局部复现、静态数据流确认、表格算术复核、派生特征实验、原始数据全链复现分别记录，不能相互替代。无标签目标允许无监督适应，须声明传导式使用范围；伪标签、置信度、分布对齐图不是真实准确率。解释图也不单独证明物理因果。
新增资料清单用validate_paper_inventory.py核验路径、PDF页数、哈希和声明阅读覆盖；通过不证明Agent确实读懂全文。历史“0篇已下载”记录保留为历史，新清单可以增加，不伪造整篇阅读状态。
''')
append(S/'SKILL.md','''
## 24. v1.6：在v1.5上继续改进
本版本保留原五模式和正式S0–S8边界。最新本地资料清单为assets/catalog/local_papers_2024_2025.json；第22节的“尚未取得论文”仅描述v1.5历史，不覆盖这个新清单。核验用scripts/validate_paper_inventory.py --manifest <清单>。
2025 E学习时读取assets/cases/2025_E_case_manifest.json、2025_E_external_code_audit.json、2025_E_paper_review_partial.json及references/2025-E-evidence-lessons.md。本案例已接触解法，不能称盲测；实际只完成派生特征诊断及局部代码/论文复核。
参考特征对照用scripts/benchmark_2025_E_reference_features.py <CSV> <输出JSON>，输出写learning_output/analyses/，不作为原版model_benchmark或正式S6 PASS。
本次用户主要要求改善Agent方法库：默认不强迫用户先答练习题，不因读过论文升级用户掌握度。用户明确练习时才启用practice的先答后反馈。
盲测初始化保留旧污染状态，冻结相同矩阵幂等、不同矩阵拒绝覆盖。它保护正常脚本流程，不能阻止手工删改或证明模型没有先验接触。旧题重新开会话不能自动恢复盲测资格。
''')
(D/'VERSION').write_text('1.6.0\n',encoding='utf-8')
append(D/'requirements.txt','PyMuPDF\n')
append(D/'README.md','''
# v1.6（当前）
本包从用户v1.5完整复制后增量修改，同时包含固定提交的上游十个Codex Skill；原始进度文档是历史记录。当前变更与验证见PROGRESS_V16.md和VALIDATION_V16.json。没有运行完整S0–S8，不能据安装依赖齐全宣称正式论文生产链通过。
''')
save(D/'UPSTREAM_LOCK.json',{'repository':'https://github.com/yushui2022/MathModel-Skill','branch':'standard','commit':'0cc261d90d21e4ed540b02b0c71018cdcd47af58','version':'2.3.0','local_extension':'1.6.0','base_archive_sha256':'4ba21e933bf73c094359b224ec1ce492a181e0b1e2daab684d7f97dd3883649b','historical_v15_exact_upstream_revision':'unknown'})
changed=[]; added=[]
for p in D.rglob('*'):
    if not p.is_file() or '__pycache__' in p.parts:continue
    rel=p.relative_to(D);old=OLD/rel
    if not old.exists():added.append(str(rel))
    elif old.read_bytes()!=p.read_bytes():changed.append(str(rel))
save(D/'V15_TO_V16_DIFF.json',{'changed':changed,'added':added,'deleted':[]})
print('assembled',len(changed),'changed files;',len(added),'added files')
