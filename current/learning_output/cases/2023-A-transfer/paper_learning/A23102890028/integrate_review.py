from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[5]
CASE=ROOT/'learning_output/cases/2023-A-transfer'
HERE=Path(__file__).resolve().parent
def read(p): return p.read_text(encoding='utf-8-sig')
def write(p,s): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def dump(p,v): write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')

supp='''## 第六篇学习落实：状态生命周期与验证边界

来源A23102890028，89页可用转换文本已读完；见[全文评审](../paper_learning/A23102890028/REVIEW.md)。本节是同题学习后的改进要求，不能用于改写冻结首答的暴露状态。

每个AP分别保存当前包的失败次数、退避阶段及剩余完整时隙。成功和最终丢弃均结束当前包，下一包从初始窗口与零失败次数开始；重置必须作用于实际使用的计数器。r次重传和总尝试r+1次在参数接口中明确区分。

发生监听忙段时，所有正在退避且能听到该发送的节点都暂停倒计时，即使原定发送时间比忙段结束更晚。交叠忙段取并集，恢复倒计时须符合DIFS和完整时隙约定。数据干扰则按真实参数生成的发送区间判断，不能沿用基础速率的固定时长。

吞吐按指定观测口径的已完成有效载荷除以实际观测时间计算。不要把未来计划发送时刻当成完成时间；并发成功按成功包数累计载荷。加入独立噪声后，除奖励变化外，还需说明重传反馈是否纳入发送概率闭合。

本轮隔离检查覆盖3个包历史序列、12个冻结样例（4个字面分支漏冻结）、3个收益系数样例（同输入下恰好两倍）和3个速率时长样例。详见[检查结果](../paper_learning/A23102890028/FINAL_CHECKS.json)。这不是完整作者程序执行，也未计算修复后的论文总吞吐。

采用论文的递进建模、双包收益、独立重复及公开失配范围的做法。Q4固定系数的基础点是标定点；跨参数验证先核对286.8/268.8等身份冲突。主解保留已有事件模型与数值，不采用尚未独立验证的系数。正式Core仍v1.41.0；本地案例版本为v8。
'''
v8=CASE/'revision_v8'
write(v8/'REFERENCE_SOLUTION.md','> 当前完整案例修订：revision_v8。已完成6/10篇全文文本评审；下方旧版本标识仅为历史记录。正式Core为v1.41.0，原作者完整程序复现0篇。\n\n'+read(CASE/'revision_v7/REFERENCE_SOLUTION.md')+'\n\n'+read(CASE/'revision_v7/CALIBRATION_SUPPLEMENT.md')+'\n\n'+supp)
write(v8/'STATE_AND_VALIDATION_SUPPLEMENT.md',supp)
write(v8/'README.md','''# 2023-A 本地参考解答 v8

完整入口：[REFERENCE_SOLUTION.md](REFERENCE_SOLUTION.md)。保留v7全文，合并第六篇校准与包状态学习。旧版标识属于历史时点；主数值未重新估计。

来源评审：[第六篇](../paper_learning/A23102890028/REVIEW.md)。校准局部重建为该目录check_calibration.py，确定性分支为finish_checks.py，输出分别为CALIBRATION_CHECKS.json、FINAL_CHECKS.json。两者只需Python标准库；本轮不重跑此前已完成的校准实验。

主解实验与验证沿用案例code和results，以及前五篇目录中已保存的检查；不要将局部检查描述成作者完整程序复现。源论文、旧版本与41项首答冻结文件保持不变。当前6/10篇全文文本评审、0篇原程序端到端复现；下一篇A23103360079（77页）。正式Core v1.41.0和45篇基线库未改版。
''')
progress='''# 当前本地学习进度（2026-09-22）

6/10篇全文文本评审完成，剩余4篇未评审；原作者完整程序复现0篇。完整案例解答为revision_v8/REFERENCE_SOLUTION.md，正式Core仍v1.41.0，45篇基线库及32/7/6划分未变化。

第六篇A23102890028的89页可用转换文本和附录已读完。已保存全文REVIEW.md、Q4校准局部重建及包历史/冻结/收益/参数化时长检查。保留递进建模、独立重复与显式校准的优点；不将标定点当独立验证，不采纳来源不一致的拟合系数。

下一步学习第七篇A23103360079（77页），逐问提取建模思路、推导、代码、结果、表达方式及可迁移限制，必要时做局部验证，再改善完整参考答案。本地Markdown已具备，无需用户提供新文件。

只在本地工作，不处理GitHub，不直接解析PDF。不得重跑已完成的六篇或改写原始论文、41项首答冻结文件、旧版解答。当前学习为同题暴露后的方法改进，不是基础模型权重训练，也尚不能证明获奖率提升。
'''
write(CASE/'PAPER_REVIEW_PROGRESS.md',progress)
write(ROOT/'learning_output/context/next_learning.md',progress)
partial=HERE/'PARTIAL_REVIEW.md'
marker='> 历史阶段记录：本篇已完成89页全文文本评审，当前结论见REVIEW.md。\n\n'
if not read(partial).startswith(marker):write(partial,marker+read(partial))
state=json.loads(read(ROOT/'PROJECT_STATE.json'))
state['current_case'].update(status='SIX_FULL_TEXT_REVIEWS_WITH_SCOPED_CHECKS',reference_solution='learning_output/cases/2023-A-transfer/revision_v8/REFERENCE_SOLUTION.md',next_action='Review A23103360079, 77 available Markdown pages; LOCAL ONLY; do not redo completed six reviews',same_problem_solution_exposure='After freeze: six full available-text reviews; remaining four not reviewed',papers_full_text_reviewed=6,partial_paper_reviews=[])
dump(ROOT/'PROJECT_STATE.json',state)
reg=json.loads(read(CASE/'PAPER_MARKDOWN_REGISTRY.json'))
for p in reg['papers']:
    if p['paper_id']=='A23102890028':p.update(status='FULL_MARKDOWN_REVIEW_PARTIAL_NUMERICAL_CHECKS',reading_scope='All 89 pages of available converted text and appendix; Q4 scalar reconstruction and calibration audit; deterministic packet-history, busy-freeze, reward and parameterized-duration probes. No original page-image inspection or full author-program execution.',review='paper_learning/A23102890028/REVIEW.md')
dump(CASE/'PAPER_MARKDOWN_REGISTRY.json',reg)
notice='> 最新状态（2026-09-22）：2023-A已完成6/10篇全文文本评审，完整参考答案为learning_output/cases/2023-A-transfer/revision_v8/REFERENCE_SOLUTION.md；第六篇A23102890028已完成。下一篇A23103360079（77页），文件已在本地。原作者完整程序复现0篇，正式Core仍v1.41.0。只做本地学习，不处理GitHub、不解析PDF。下方较早状态仅作历史记录，以PROJECT_STATE.json和最新进度为准。\n\n'
for name in ['START_HERE.md','HANDOFF_NEXT_CHAT.md','NEW_CHAT_PROMPT.md']:
    p=ROOT/name
    if not read(p).startswith(notice):write(p,notice+read(p))
freeze=json.loads(read(CASE/'FIRST_ANSWER_FREEZE.json'))
bad=[name for name,digest in freeze['files'].items() if hashlib.sha256((CASE/name).read_bytes()).hexdigest()!=digest]
source_bad=[]
for p in reg['papers']:
    for kind in ['markdown','raw_layout']:
        if hashlib.sha256((ROOT/p[kind+'_repo_path']).read_bytes()).hexdigest()!=p[kind+'_sha256']:source_bad.append(p['paper_id']+':'+kind)
assert not bad and not source_bad
assert sum(p['status']=='FULL_MARKDOWN_REVIEW_PARTIAL_NUMERICAL_CHECKS' for p in reg['papers'])==6
for p in [v8/'REFERENCE_SOLUTION.md',HERE/'REVIEW.md',HERE/'FINAL_CHECKS.json',HERE/'CALIBRATION_CHECKS.json']:assert p.is_file()
result=dict(status='PASS',frozen_files_checked=len(freeze['files']),frozen_mismatches=bad,source_text_files_checked=20,source_mismatches=source_bad,papers_full_text_reviewed=6,author_full_program_reproductions=0,reference_solution=str(v8/'REFERENCE_SOLUTION.md'))
dump(HERE/'REVIEW_VALIDATION.json',result)
print(json.dumps(result,ensure_ascii=False))
