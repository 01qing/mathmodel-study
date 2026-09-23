"""Package completed paper review. Standard library; no rerun of simulations."""
from pathlib import Path
import json, hashlib, shutil
HERE=Path(__file__).resolve().parent
CASE=HERE.parents[1]
ROOT=CASE.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

checks=read(HERE/'CHECKS.json')
freeze=read(CASE/'FIRST_ANSWER_FREEZE.json')
assert all(sha(CASE/p)==h for p,h in freeze['files'].items())
archive=ROOT/'learning_output/cases/2023A_first_answer_v1_frozen.zip'
assert sha(archive)==freeze['sha256']
registry=read(CASE/'PAPER_MARKDOWN_REGISTRY.json')
for p in registry['papers']:
    target=ROOT/'learning_sources/2023A_markdown'/p['paper_id']
    target.mkdir(parents=True,exist_ok=True)
    for key,hashkey in [('markdown_path','markdown_sha256'),('raw_layout_path','raw_layout_sha256')]:
        source=Path(p[key]);dest=target/str(p[key]).replace('\\','/').split('/')[-1]
        if not dest.exists():shutil.copyfile(source,dest)
        assert sha(dest)==p[hashkey]
        p[key.replace('_path','_repo_path')]=dest.relative_to(ROOT).as_posix()
    if p['paper_id']=='A23100070049':
        p.update(status='FULL_MARKDOWN_REVIEW_PARTIAL_NUMERICAL_CHECKS',
                 reading_scope='56 Markdown pages, selected raw-layout, appendix static audit, formula/branch probes and four-topology simulations; original MATLAB not run',
                 review='paper_learning/A23100070049/REVIEW.md')
registry['portable_root']='learning_sources/2023A_markdown'
registry['path_base_in_git_repository']='current/'
registry['path_resolution']='Prefer *_repo_path relative to project root current/; original *_path retained only as source provenance.'
save(CASE/'PAPER_MARKDOWN_REGISTRY.json',registry)
(ROOT/'learning_sources/2023A_markdown/README.md').write_text('# 用户提供的 2023-A 论文 Markdown\n\n10 篇正文及 raw_layout，与原登记 SHA256 一致。复制文件不代表读取或完成评审。只保留文本，不包含 PDF 和页面图片，故原文中的图片回退链接在本目录不可用。公式不完整时先查 raw_layout，再告知用户具体缺失页；禁止直接解析 PDF。阅读进度以项目状态及案例进度文件为准。\n',encoding='utf-8')

revision=CASE/'revision_v3';revision.mkdir(exist_ok=True)
base=(CASE/'revision_v2/REFERENCE_SOLUTION.md').read_text(encoding='utf-8')
# Preserve the v2 file, but make the new copy's image paths portable on GitHub.
base=base.replace(CASE.as_posix()+'/deliverables/','../deliverables/')
base=base.replace('当前已读第一篇同题论文','该修订时点已读第一篇同题论文')
text=['\n\n# 第二篇学习后的补充：问题四的条件化答案\n',
      '论文 A23100070049 第 9、31–34 页将题目未给定的相邻干扰关系分情况讨论。本修订在原有假设和主结果之外补齐此项，所有新结果均来自已有 CHECKS.json，不替换学习前冻结结果。\n',
      '## 参数与事件定义\n',
      '互听图固定为 AP1–AP2–AP3，AP1/AP3 交叠成功；两条相邻边的干扰分别开关，且每条边假设双向对称。速率 455.8 Mbps，CWmin=16、CWmax=1024、r=32、Pe=0；每种情形 5 个种子（101、202、303、404、505），预热 0.5 秒后观测 5 秒，保持原来的虚拟交换忙时语义。\n',
      '## 数值答案\n']
labels=['两条边都干扰','仅 AP1–AP2 干扰','仅 AP2–AP3 干扰','两条边都不干扰']
for label,r in zip(labels,checks['topology_cases']):
    vals='、'.join(f'{x["mean"]:.3f}' for x in r['per_node'])
    text.append(f'- {label}：总吞吐量 **{r["total"]["mean"]:.3f} ± {r["total"]["ci95_halfwidth"]:.3f} Mbps**；AP1、AP2、AP3 分别为 {vals} Mbps，平均 Jain 指数 {r["fairness"]["mean"]:.4f}。\n')
text += ['\n± 为 5 个种子均值的 95% t 区间半宽，df=4，不含模型误差。两侧都干扰的 5 秒结果与原主实验 10 秒结果略有不同，不能将其理解为改写原主实验。\n',
         '\n中间两种情形通过交换 AP1/AP3 在模型结构上等价；样本总均值相差 0.048 Mbps，逐节点均值交换后也接近。有限样本不要求轨迹相同，置信区间重叠也不等于严格等价性检验。\n',
         '\n四种情形中 AP2 均获得较少发送机会；即使相邻并发不再失败，互听冻结仍使中心 AP 处于不利位置。这说明“避免碰撞”与“公平分配信道”是不同目标。上述四种情形未覆盖单向干扰和捕获效应，不能宣称穷尽所有物理配置。\n',
         '\n## 验证和选模\n',
         '20 次运行已经完成，另外四条短轨迹共 29789 项独立断言通过，涵盖交叠结果、退避阶数、完整时隙、DIFS 和有效载荷计数。独立重放只覆盖短轨迹，原 MATLAB 未运行。事件仿真仍是主要数值方案，非对称固定点是后续解析候选，理想无碰撞活动集仅用于机制解释。\n',
         '\n## 问题二的奖励核查\n',
         '第二篇公式 (6.2.4) 采用 2τ(1−τ) 作为成功包数期望，漏掉双发双成功奖励 2τ²；计算得 62.25747 Mbps，与作者 62.26 一致。加回奖励的独立近似为 70.55846 Mbps；我们的残余计数链为 68.94875 Mbps，更接近原仿真 68.95272 Mbps。因此继续保留残余计数链，不采用作者报告值替换答案。\n',
         '\n完整评审见 [第二篇记录](../paper_learning/A23100070049/REVIEW.md)，实验见 [CHECKS.json](../paper_learning/A23100070049/CHECKS.json)。两篇均已完成文本评审和局部数值检查，均未完整复现作者代码。正式 Core 仍为 v1.41。\n']
(revision/'REFERENCE_SOLUTION.md').write_text('> 当前为案例修订 v3。包含原解答、第一篇的诊断补充和文末第二篇的条件化分析。历史冻结时点的“未读同题论文”只适用于当时。\n\n'+base+''.join(text),encoding='utf-8')
(revision/'README.md').write_text('# 案例修订 v3\n\n主入口 REFERENCE_SOLUTION.md。新模型实验与数值在 ../paper_learning/A23100070049/CHECKS.json；复算运行同目录 run_checks.py，通常无需重跑。主仿真代码与学习前冻结结果未修改。finalize_review.py 仅检查来源/冻结哈希、复制缺少的源文本并生成修订及状态。首次迁移源文本需要本地原文件，仓库已有副本后可直接复用。\n',encoding='utf-8')
state=read(ROOT/'PROJECT_STATE.json')
state['current_case'].update(status='TWO_PAPER_TEXT_REVIEWS_AND_TOPOLOGY_REVISION_COMPLETE',
 reference_solution='learning_output/cases/2023-A-transfer/revision_v3/REFERENCE_SOLUTION.md',
 papers_full_text_reviewed=2,papers_end_to_end_reproduced=0,
 same_problem_solution_exposure='After freeze: A23104220005 and A23100070049 full Markdown reviews completed; other 8 unread',
 next_action='Read A23102470073 by question using repository Markdown; prioritize Q3 analytic reconstruction and Q4 timing/topology. Do not rerun completed first two papers.')
state['portable_source_root']='learning_sources/2023A_markdown'
save(ROOT/'PROJECT_STATE.json',state)
progress='''# 2023-A 当前进度（2026-09-22）

10 篇 Markdown 已登记并复制到仓库；2 篇全文文本评审完成，8 篇未读。原作者完整复现为 0 篇。论文注册表优先使用 *_repo_path，旧绝对路径仅用于来源追踪。

- A23104220005：49 页；逐问评审、局部调度探针、连续窗口验证已完成；成果 revision_v2。
- A23100070049：56 页；评审、四种干扰情形的 20 次运行、四条短轨迹独立验证已完成；成果 revision_v3。不要把此前中断时的“待收尾”作为当前状态。

下一篇 A23102470073，按 Q1–Q4 与前两篇横向比较，重点补 Q3 解析式的可恢复性和 Q4 时间语义。遇到缺公式先读 raw_layout，仍不清楚再说明缺失页，由用户转 Markdown；禁止解析 PDF。

当前完整解答：revision_v3/REFERENCE_SOLUTION.md。正式 Core v1.41、旧 45 篇基线计数不变。2022-C 已完成，不重启。获奖率提升未验证。
'''
(CASE/'PAPER_REVIEW_PROGRESS.md').write_text(progress,encoding='utf-8')
(ROOT/'learning_output/context/next_learning.md').write_text(progress+'\n项目根入口另见 HANDOFF_NEXT_CHAT.md。\n',encoding='utf-8')
start=ROOT/'START_HERE.md'
s=start.read_text(encoding='utf-8'); marker='最新进展：A23104220005'
if marker in s:s=s[:s.index(marker)]
start.write_text(s+'最新进展：两篇文本评审及案例修订 v3 已完成，完整解答在 `learning_output/cases/2023-A-transfer/revision_v3/REFERENCE_SOLUTION.md`。下一篇 A23102470073。网页接续先读 `HANDOFF_NEXT_CHAT.md`，所有 10 篇 Markdown 的仓库路径已登记；不要重跑已完成的实验。\n',encoding='utf-8')
save(HERE/'REVIEW_VALIDATION.json',dict(frozen_files_unchanged=len(freeze['files']),frozen_zip_unchanged=True,
 markdown_copies_hash_verified=20,source_experiment_sha256=sha(HERE/'CHECKS.json'),
 short_trace_assertions=sum(x['checks'] for x in checks['short_trace_validation']),
 source_simulator_sha_matches=sha(CASE/'code/wlan.py')==checks['source_sha256']['wlan.py'],
 author_matlab='NOT_RUN',original_images='NOT_VIEWED'))
print('Review finalized; 20 Markdown copies and frozen files verified; revision_v3 saved.')
