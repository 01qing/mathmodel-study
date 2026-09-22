"""Build learning deliverables and update local progress, preserving frozen v1."""
from pathlib import Path
import json, hashlib, statistics, re
HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
ROOT = CASE.parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
data = json.loads((HERE/'LEARNING_CHECKS.json').read_text(encoding='utf-8'))
freeze = json.loads((CASE/'FIRST_ANSWER_FREEZE.json').read_text(encoding='utf-8'))
checks = {name:sha(CASE/name)==expected for name,expected in freeze['files'].items()}
assert all(checks.values())
assert sha(Path(freeze['archive'])) == freeze['sha256']
registry_path = CASE/'PAPER_MARKDOWN_REGISTRY.json'
registry = json.loads(registry_path.read_text(encoding='utf-8'))
paper = next(p for p in registry['papers'] if p['paper_id']=='A23104220005')
assert sha(Path(paper['markdown_path'])) == paper['markdown_sha256']
assert sha(Path(paper['raw_layout_path'])) == paper['raw_layout_sha256']
raw = Path(paper['raw_layout_path']).read_text(encoding='utf-8')
pages = re.split(r'## Page (\d+)\n',raw)
appendix = ''.join('## Page '+pages[i]+'\n'+pages[i+1] for i in range(1,len(pages),2) if int(pages[i])>=38)
(HERE/'AUTHOR_APPENDIX_EXTRACT.md').write_text('# Converted appendix text; not an executable MATLAB bundle\n\n'+appendix,encoding='utf-8')
summary=[]
for q in range(1,5):
    runs=[r for r in data['continuous_windows'] if r['q']==q]
    node_windows=[row for r in runs for row in r['windows_per_node_mbps']]
    values=[sum(row) for row in node_windows]
    summary.append(dict(question=q,mean_total_mbps=statistics.mean(values),
        observed_window_total_min=min(values),observed_window_total_max=max(values),
        node_min=[min(row[i] for row in node_windows) for i in range(len(node_windows[0]))],
        node_max=[max(row[i] for row in node_windows) for i in range(len(node_windows[0]))],
        minimum_window_jain=min(r['minimum_window_jain'] for r in runs),
        mean_failure_fraction=statistics.mean(r['completed_attempt_failure_fraction'] for r in runs)))
lines=['\n\n# 学习第一篇论文后的补充验证（案例修订 v2）\n',
       '本节是读取 A23104220005 后新增，前文保留学习前四问推导和主结果。正式 Core 仍为 v1.41。新增的是验证与论证，不宣称更高获奖率。\n',
       '## 连续窗口与节点分配\n',
       '采用原仿真器和原基准参数，种子 101、202、303、404、505；每次先预热 0.5 秒，再连续观察 10 秒，以完成时刻统计每秒成功载荷。下列区间为实际观察到的 50 个窗口最小/最大值，不是置信区间，也不是理论上下界。\n']
for r in summary:
    lines.append(f"- 第 {r['question']} 问：平均 {r['mean_total_mbps']:.5f} Mbps；每秒总量范围 {r['observed_window_total_min']:.3f}–{r['observed_window_total_max']:.3f} Mbps；平均完成尝试失败比例 {r['mean_failure_fraction']:.2%}。\n")
r=summary[3]
lines += [f"\n第 4 问 AP2 每秒吞吐量为 {r['node_min'][1]:.3f}–{r['node_max'][1]:.3f} Mbps；AP1 为 {r['node_min'][0]:.3f}–{r['node_max'][0]:.3f}，AP3 为 {r['node_min'][2]:.3f}–{r['node_max'][2]:.3f} Mbps。最小每秒 Jain 指数为 {r['minimum_window_jain']:.4f}。在本次有限轨迹中，中心节点持续受到挤占；不能推广为所有时间尺度下的严格饿死结论。\n",
          '\n20 次运行逐节点窗口累计成功包数与整段结果完全一致，完成尝试与失败计数也一致。相邻窗口可能相关，因此原先基于独立种子的置信区间仍使用种子级均值，不能拿窗口数扩充独立样本量。失败比例以包为单位，既包含独立噪声也可能包含碰撞；本输出没有分离两者。\n',
          '\n## 与论文数值不一致时如何处理\n',
          '论文第二问的独立性近似约 70.56 Mbps 已算出；我们的残余计数链约 68.94875 Mbps，与冻结仿真 68.95272 Mbps 相符，继续保留该路线。第一问固定点 67.1744 与仿真 65.24496 的正偏差仍须明确承认。第三、四问不强行贴合论文数值，先核对碰撞窗口、非对称拓扑和成功计数语义。\n']
for q in [1,2]:
    means=[statistics.mean(p['total_mbps'] for p in data['deadline_probes'] if p['q']==q and p['tolerant']==t) for t in [False,True]]
    lines.append(f"\n第 {q} 问的独立调度探针：精确浮点相等版本平均 {means[0]:.5f} Mbps，容差分组版本 {means[1]:.5f} Mbps。它只验证累计时刻比较这一机制的敏感性，采用 Python 随机数及统一边界，不是论文 MATLAB 数值的复现，也不足以解释全部差异。\n")
lines += ['\n## 学习落地和剩余问题\n',
          '从论文第 16–17、26–29、33 页采纳“总量＋逐节点分布＋参数偏差方向”的证据结构。我们将重新初始化的短仿真和连续时间窗口明确区分，并为成功分支增加统计守恒验证。完整逐问评审见 ../paper_learning/A23104220005/REVIEW.md，运行数据见 LEARNING_CHECKS.json。\n',
          '作者第三问关键公式 (32) 在两份 Markdown 中仍缺失；原 MATLAB 与原图尚未复现。后续横向比较另外 9 篇，重点寻找隐藏节点时间语义、链状拓扑解析和代码验证证据。遇到需要原 PDF 内容时，先说明所需页码，由用户提供 Markdown。\n']
revision=CASE/'revision_v2';revision.mkdir(exist_ok=True)
baseline_text=(CASE/'REFERENCE_SOLUTION.md').read_text(encoding='utf-8')
baseline_text=baseline_text.replace('](deliverables/', ']('+CASE.as_posix()+'/deliverables/')
preface='> 案例修订 v2：前文保留学习前冻结解答，其中“未读同题解答”等表述仅指冻结时点。当前已读第一篇同题论文；新增学习与验证见文末。图片链接已调整到原文件位置。\n\n'
(revision/'REFERENCE_SOLUTION.md').write_text(preface+baseline_text+''.join(lines),encoding='utf-8')
save(revision/'LEARNING_SUMMARY.json',dict(scope='diagnostic and exposition revision; main model unchanged',summary=summary,source_paper='A23104220005',runs=20,probe_runs=20,frozen_files_unchanged=checks,archive_hash_unchanged=True))
(revision/'README.md').write_text('''# 2023-A 案例修订 v2

REFERENCE_SOLUTION.md 是完整参考解答，末尾追加第一篇优秀论文带来的验证改进。不是新 Core 发布，不覆盖学习前冻结包。

复算：用 Python 3 运行 `../paper_learning/A23104220005/run_learning_checks.py`（标准库，无新增依赖），再运行同目录 `save_learning.py`。前者调用冻结版 code/wlan.py，运行 20 个调度探针及 20 条连续仿真轨迹，后者验证冻结文件和来源哈希后生成本目录。

原四问主计算入口和参数见 ../code/run_experiment.py；本修订不需要重跑全部主场景。所有新增每秒数据在 ../paper_learning/A23104220005/LEARNING_CHECKS.json。作者 MATLAB 未执行，局部 Python 探针不得称为原作者完整复现。
''',encoding='utf-8')
paper.update(status='FULL_MARKDOWN_REVIEW_PARTIAL_NUMERICAL_CHECKS',reading_scope='All 49 Markdown pages; selected raw-layout pages; appendix static review; our bounded Python probes; no image or MATLAB reproduction',review='paper_learning/A23104220005/REVIEW.md')
save(registry_path,registry)
(CASE/'PAPER_REVIEW_PROGRESS.md').write_text('''# 2023-A Markdown 论文对照进度

2026-09-22：10 篇已登记，其中 A23104220005 完成 49 页全文 Markdown 与附录的文本评审、关键页 raw_layout 核对；其余 9 篇未读。没有解析 PDF。

已运行 20 个局部调度探针和 20 条连续仿真轨迹；窗口累计与整段包数守恒检查通过。原 MATLAB、原图及完整隐藏节点公式尚未复现，不能计为全流程复现。

本轮成果：paper_learning/A23104220005/REVIEW.md、LEARNING_CHECKS.json、revision_v2/REFERENCE_SOLUTION.md。采纳逐节点分布、连续窗口及有符号偏差的证据组织；四问主模型和冻结值不变。学习前 ZIP 与全部冻结文件哈希再核对一致。

下一篇按目录顺序 A23100070049，与第一篇按 Q1–Q4 横向比较，优先补足 Q3 隐藏节点时间语义和 Q4 非对称拓扑分析。正式 45 篇基线计数及 Core v1.41 不变，新增学习单独记录。奖项仍未独立核验。
''',encoding='utf-8')
state_path=ROOT/'PROJECT_STATE.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
state['current_case'].update(status='FIRST_PAPER_TEXT_REVIEW_AND_DIAGNOSTIC_REVISION_COMPLETE',
    reference_solution='learning_output/cases/2023-A-transfer/revision_v2/REFERENCE_SOLUTION.md',
    same_problem_solution_exposure='After freeze: A23104220005 all 49 Markdown pages reviewed; 9 other registered papers unread',
    next_action='Review A23100070049 by question, prioritizing Q3 hidden timing and Q4 asymmetric topology; no direct PDF extraction',
    papers_full_text_reviewed=1,papers_end_to_end_reproduced=0)
save(state_path,state)
(ROOT/'learning_output/context/next_learning.md').write_text('''# 下一步（2026-09-22）

2023-A 第一篇 A23104220005 已完成全文 Markdown 文本评审和局部数值检查，非完整原作者复现。10 篇中 1 篇文本评审完成，9 篇未读。案例修订 v2 已加入连续窗口、逐节点分配与守恒验证；无需重跑第一篇或旧 2022-C。

下一篇 A23100070049：按子问与第一篇和冻结答案横向比较，重点研究 Q3 隐藏节点碰撞时段、Q4 非对称拓扑与公平性。当前参考解答为 learning_output/cases/2023-A-transfer/revision_v2/REFERENCE_SOLUTION.md。旧冻结文件与 ZIP 保持不变。

论文来源和哈希见 PAPER_MARKDOWN_REGISTRY.json；第一篇具体证据见 paper_learning/A23104220005/REVIEW.md。新经验卡位于 knowledge_base/competition_lessons/2023A_timing_and_window_evidence.md，不自动混入已评审 Train 检索库，不算新 Core 发布。

不得直接解析 PDF。两份 Markdown 无法恢复第一篇公式 (32)，若后续确需复现该式，再说明第 25 物理页的公式缺失，请用户补 Markdown；目前继续学习其他论文不受阻塞。
''',encoding='utf-8')
save(HERE/'SOURCE_AND_VALIDATION.json',dict(paper_markdown_sha256=paper['markdown_sha256'],raw_layout_sha256=paper['raw_layout_sha256'],appendix_extract_sha256=sha(HERE/'AUTHOR_APPENDIX_EXTRACT.md'),frozen_files_checked=len(checks),frozen_files_unchanged=all(checks.values()),frozen_archive_unchanged=True,diagnostic_runs=20,probe_runs=20,window_conservation_checks='PASS',author_matlab_execution='NOT_RUN',original_figure_visual_review='NOT_RUN'))
print(json.dumps(summary,ensure_ascii=False,indent=2))
