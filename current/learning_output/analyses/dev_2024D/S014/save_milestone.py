from pathlib import Path
import json,hashlib,datetime,zipfile,shutil
O=Path(__file__).resolve().parent;W=O.parents[3];P=W.parent;C=P/'clean-dev-2024D';B=C/'v1.39-release-work'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
val=json.loads((O/'VALIDATION_S014.json').read_text(encoding='utf-8'));assert val['status']=='PASS'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(O/'VALIDATION_S014.md').write_text('''# S014 验证范围

本轮状态：S014_DEV_REVIEW_COMPLETE_R2。v1.40-work NOT SEALED。

- 局部数学/代码审计：最终30/30 PASS。保留首轮28/29的FAIL：审计方误以为印刷AHP权重是特征向量舍入值；随后按列归一化均值恢复其原语。正文/代码中原有错误没有被抹去。
- 专项结构与保护：VALIDATION_S014.json中18项检查通过，包括4份主要子问竞争卡、29条Registry记录、62页文本/视觉记录、七门检查和R2边界。
- 已选跑的继承项：v1.39数据合同、v1.9训练回归、工作区检查、2025-A与2025-F检索smoke均exit0。详细输出保留为同目录log。没有将本轮称为全部22套历史测试重跑。
- v1.39封存内容1788文件逐项SHA256未变；独立解答55文件与冻结manifest哈希未变。
- 45篇的32Train/7Dev/6Test划分未变，split_manifest和chunks与稳定版字节一致；6752chunks数量沿用该相同文件的封存验证，本轮不重新打开保护论文做roundtrip。检索仍限定reviewed Train。只更新S014的Dev评审元数据。
- S015/S016未在本轮打开。历史catalog记录S014所在集合曾有片段暴露，故不把历史pristine状态升级成已证明。本轮只证明独立解答冻结先于本轮S014全文暴露。
- 此前Test已在独立答案冻结后完成评价，不能重新称freshblind；本轮不向Core推广Test内容。

这些PASS仅支持局部算术、错误检出、资产一致性与保护边界。作者全链复现NOT_RUN；独立模型增益NOT_ESTABLISHED；No-Core/Previous-Core/New-Core NOT_RUN。S015/S016、完整2024-D最终方法图、题组Mini Transfer和v1.40规则发布仍待后续完成。
''',encoding='utf-8')
state=dict(status='IN_PROGRESS_NOT_SEALED',base='1.39.0 SEALED',updated_at=now,current_milestone='S014_DEV_REVIEW_COMPLETE_R2',current='S014',next='S015 / 2024-D / Dev',next_papers_not_opened=['S015','S016'],scope='S014 full review and local audit; candidate rules not yet promoted;2024-Dgroup2of4',stable_core_changed=False,working_metadata_changes=['S014 reviewer catalog','S014 retriever Dev status'],core_gain='NOT_ESTABLISHED',ablation='NOT_RUN',historical_pristine='UNVERIFIED',test_exposure='2024-F and2025-D already evaluated after independent freezes; notfreshblind; noTestknowledgepromotioninthisincrement',evidence='learning_output/analyses/dev_2024D/S014/S014_FINAL_REVIEW.md',validation='learning_output/analyses/dev_2024D/S014/VALIDATION_S014.json',inherited_release_files_scope='VERSION/PROGRESS_V139/RELEASE_MANIFEST_V139 describe baseline only; not v140 release')
dump(W/'DEVELOPMENT_STATE_V140.json',state)
(W/'PROGRESS_V140.md').write_text('''# v1.40 开发进度：NOT SEALED

唯一正式稳定版仍为MathModel-Core v1.39.0。此工作目录由v1.39增量创建；复制来的VERSION、v1.39发布manifest及历史SKILL状态文字仅描述历史基线，不证明v1.40封版，也不能覆盖本文件与DEVELOPMENT_STATE_V140.json的新进度。

S014 / 2024-D / Dev现已完成62/62页全文和原PDF视觉审查、53–62页打印代码静态审计，等级R2。已保存4问方法竞争、6小时Baseline、可迁移模块、错误模式、29条统一Result Registry记录、S013/S014阶段方法图、七门兼容性检查与30/30局部审计。首次FAIL与原因、修复、复测完整保留。

稳定Core规则未改。本轮只更新工作副本中S014的Dev评审元数据；规则扩展保存在RULE_CANDIDATES_V140.md，尚未发布。已有实体、时间、指标、组合规则优先复用，不复制角色Skill或平行知识库。

下个执行位置：S015 / 2024-D / Dev，继续用既有冻结独立解答作比较基准；不重新独立作答，不倒改冻结结果。再完成S016，最终合并四篇方法图与题组Mini Transfer，审查去重后的通用规则，跑与实际变更相匹配的完整发布验证后才考虑v1.40封存。

32/32Train完成；2024-D仅S013/S014两篇完成。S015/S016本轮未读。Test已在历史独立冻结后评价，不是freshblind；不要把Test比较内容用于本次Core增量。历史pristine仍UNVERIFIED。Regression/Audit PASS不等于Core能力提升；cleanblind gain NOT_ESTABLISHED，三条件Core ablation NOT_RUN。

主要成果：learning_output/analyses/dev_2024D/S014/S014_FINAL_REVIEW.md；验证：同目录VALIDATION_S014.md。稳定v1.39的1788文件及冻结独立解答55文件均已核验未改。
''',encoding='utf-8')
state.update(stage_status='S014_STAGE_CLOSED',execution_status='STOPPED_AT_USER_REQUEST',next='STOP; do not open new papers until user resumes',resume_candidate='S015 / 2024-D / Dev')
dump(W/'DEVELOPMENT_STATE_V140.json',state)
with (W/'PROGRESS_V140.md').open('a',encoding='utf-8') as f:
    f.write('\n## 本次阶段封口\n\n用户要求完成此次封口、先不开新的。S014_STAGE_CLOSED；当前停止，不打开S015/S016。前文下个执行位置仅为未来恢复候选，不代表继续执行授权。v1.40仍NOT SEALED，v1.39仍为稳定版。\n')
(O/'STAGE_CLOSURE.md').write_text('''# S014 阶段封口

状态：S014_STAGE_CLOSED。用户要求先不开新的，本阶段完成后停止；S015/S016保持未读。

交付已完成：62页全文与原PDF视觉审查、附录静态审计、4问完整方法竞争、29条Result Registry、阶段方法图与七门检查、局部审计最终30/30及首轮FAIL历史、选定历史兼容和检索保护验证。

冻结保护：v1.39的1788文件、独立解答55文件未改。增量恢复包包含本次资产、元数据及状态文件，使用SHA256和ZIP逐文件校验；须叠加到新建的已校验v1.39副本，不覆盖稳定版。

本次没有发布v1.40正式版。候选规则仍未进入稳定Core；S015/S016、四篇最终方法图、题组Mini Transfer与v1.40最终发布验证仍未完成。既有Test暴露不能改称freshblind；局部PASS不代表Core能力增益。
''',encoding='utf-8')
external=C/'CURRENT_STATE.json';prior=json.loads(external.read_text(encoding='utf-8'))
backup=C/'CURRENT_STATE_before_S014_20260913.json'
if not backup.exists():shutil.copy2(external,backup)
prior['development_v140']=dict(state=state,workspace=str(W),progress=str(W/'PROGRESS_V140.md'))
dump(external,prior)
# Incremental recovery archive, not a sealed release. Includes all changed/new files.
base={r:h for h,r in (line.split('  ',1) for line in (B/'FILES_V139.sha256').read_text(encoding='utf-8').splitlines() if line.strip())}
payload=[]
for f in sorted(W.rglob('*')):
    if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc':
        rel=f.relative_to(W).as_posix()
        if rel not in base or sha(f)!=base[rel]:payload.append(f)
files={f.relative_to(W).as_posix():dict(sha256=sha(f),bytes=f.stat().st_size) for f in payload}
manifest=dict(kind='INCREMENTAL_RECOVERY_NOT_RELEASE',status='NOT_SEALED',base_zip='Graduate-MathModel-Learning-Skill-v1.39.zip',base_zip_sha256='b6c47da3a61c16e9ac3cf1ec2e834d05951db60ea4fd7854762d7ee456feef82',restore='Extract verifiedv1.39 into NEW v1.40-work; overlay worktree/ from this archive; never overwrite sealedv1.39. Read DEVELOPMENT_STATE_V140.json. No files deleted by this increment.',files=files,created_at=now)
dest=P/'v140-recovery';dest.mkdir(exist_ok=True);z=dest/'MathModel-Core-v1.40-S014-work-recovery.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
    out.writestr('RECOVERY_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    for f in payload:out.write(f,'worktree/'+f.relative_to(W).as_posix())
with zipfile.ZipFile(z) as src:
    assert src.testzip() is None
    for rel,d in files.items():assert hashlib.sha256(src.read('worktree/'+rel)).hexdigest()==d['sha256'],rel
digest=sha(z);(dest/(z.name+'.sha256')).write_text(digest+'  '+z.name+'\n',encoding='utf-8')
dump(dest/'RECOVERY_STATE.json',dict(status='RECOVERY_VERIFIED_NOT_SEALED',archive=str(z),sha256=digest,files=len(files),milestone='S014_STAGE_CLOSED_R2',next='STOP_AT_USER_REQUEST_NO_NEW_PAPERS',base_zip_sha256=manifest['base_zip_sha256']))
print(json.dumps(dict(archive=str(z),sha256=digest,files=len(files),bytes=z.stat().st_size,status='RECOVERY_VERIFIED_NOT_SEALED'),ensure_ascii=False))
