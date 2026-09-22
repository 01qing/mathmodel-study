# v1.41工作断点与自动续办

用户明确授权自主完成：A题复盘→S015/S016 Dev题组学习→未接触答案的新任务验证。A整题不要继续。v1.40唯一稳定封存版不改。本目录由v1.40完整复制，旧PROGRESS/manifest仅是基线历史，当前NOT_SEALED以WORK_STATUS_V141.json为准。

自动续办任务ID：mathmodel-core-v1-41，PAUSED，用户取消定时，当前对话直接执行，不再创建定时。全部目标完成后用automation_update暂停它，不扩展无限训练。无变化不通知，重要里程碑/失败/必须用户输入才通知。当前轮已完成实质A复盘并开始S015，不要从头重复。

## 已完成

- A候选规则：learning_output/analyses/practice_A_retrospective/RULE_CANDIDATES.md。
- 独立小测试：同目录independent_tests.py与INDEPENDENT_TEST_RESULTS.json；7项局部测试通过，含合成故障对照与独立平板解析解。非Core消融，非盲测。第7条实际输入CSV账本缺口尚无集成回归。
- 2024-D原独立解答：learning_output/analyses/dev_2024D_presolution/，freeze manifest55文件全部hash一致，核验后才访问新Dev。
- S015/S016源PDF已由source_index路径定位且hash一致，复制到learning_output/analyses/dev_2024D/S015和S016/source.pdf；全文文本已提取到full_text.txt。提取不是阅读。两篇96+114=210页。
- S015文本96/96已阅读；视觉已核验13、14、25、26、39、41、61、73、93、95、96共11/96页，图片在visual/。详见S015/PARTIAL_REVIEW.md。
- S016只读第1页封面。还未读正文。

## 下一批具体工作

1. S015全文文本已完成，继续未看页面的原PDF视觉审查；按页保存实际阅读账本。全文、图表、代码各自核验。每次工具输出控制页数，避免截断后声称全文读过。
2. 视觉覆盖必须真实完成，可分批渲染并查看，不能用OCR代替。优先13–14已核验发现后，推进其余页。
3. S015公式(2-2)漏平方、表2-2 RYs=sum而称方差已定位到PDF13/14/88；按合成数据与表格算术重放，保护作者字段与我们重实现的区别。分类样本分母、目标泄漏、预测年份等仍待追溯，不提前下全篇结论。
4. S015完成四问卡、统一Registry、模型竞争/6hBaseline/模块/错误模式/严格R0-R7/视觉独立状态后再推进S016；两篇必须完成才能称2024-D四篇闭环。
5. 从基线查找S013旧资产及S014资产，按同目标/支持域/时间/评价器形成四篇最终方法图、七门Composer、题组Mini Transfer。不得用不同作者任务的高分强比原冻结解答。严禁追改原冻结解答。
6. 新规则仅进v1.41-work，去重已有规则。生产工具修复必须只改工作版并做真实集成与历史回归。baseline完整树与freeze文件hash需再次核验。
7. 最后选真正未看答案的新任务先固定任务/评价规则并冻结方案再执行；自造开发小例子不夸成独立Core提升。严格三条件Core消融没有相同模型/提示/工具/预算/评价器的调用环境则NOT_RUN并解释。不要调用子代理（用户未授权委派）。

## 环境

普通python有numpy/scipy/pymupdf；捆绑Python有openpyxl/docx但无scipy。Excel只读使用捆绑路径C:/Users/lingyun/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe。中文输出加-X utf8。冻结Core中的原Skill说明继续适用。

当前NOT_SEALED，不可发布、宣称210页完成、重新使用已暴露Test为盲测。所有未完成项必须留在状态文件。不要因用户离线而跳过必要审查。

## 最新执行断点

定时已按用户指示PAUSED。S015文本96/96，原PDF视觉45/96（具体页码见JSON），局部算术/机制审计17/17通过，非复现或能力PASS。AUDIT_FINDINGS.md及RESULT_REGISTRY_PARTIAL.json已落盘。继续剩余页40、42–60、62–72、74–92、94的视觉；S016尚未正文学习。下一步补四问竞争卡和源码语义映射。

## 2026-09-14更新（覆盖前述页面断点）

S015文本96/96、原PDF视觉96/96已完成，PAGE_AUDIT_LEDGER.json记录逐页证据。QUESTION_COMPETITION.md已完成四问竞争、6hBaseline、模块、错误模式、R2边界及本篇七门检查。尚未整合Core/最终Registry/全量回归。S016正文仍未读，下一步开始；不从头重复S015。

## S016最新断点

文本114/114已实际阅读，视觉6/114（22、29、42、87、104、112）。PARTIAL_REVIEW.md已记录四问及全部打印代码发现。优先完成剩余视觉，再构建审计和四问卡。关键是p22/p87结果冲突、p29土地守恒、p104错期文件、p42上下尾、p112归因实际原语。原打印附录没有完整LSTM/XGB/RF训练链。不可直接继承或宣称全篇完成。

S016首批审计19/19通过（表格算术/数学反例，非作者复现）。附录2015—2020六年LSTM重放MAE=12.0317267mm、RMSE=17.1023934mm；不是独立留出评估。土地15个恒等式中前5符合舍入精度，后10不闭合。数据及记录已落盘RESULT_REGISTRY_PARTIAL.json。下一步补S016剩余108页视觉、四問竞争、去重规则，之后题组方法图/组合/迁移及真实集成回归；不得提前封版。
