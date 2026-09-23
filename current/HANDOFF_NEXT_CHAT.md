> 当前入口已部署（2026-09-22）：共享Core + mathmodel-architect解题 + mathmodel-reviewer审查，默认顺序执行解题、审查、修正与复核。等待用户提供新题，暂停新论文学习。技能与交接完整性检查通过，真实新题尚未运行，非独立多智能体系统。正式Core仍v1.41.0。入口协议：C:/Users/lingyun/.codex/skills/mathmodel-evidence/references/solve-review.md。

> 最新状态（2026-09-22）：2023-A的10/10篇可用全文文本已学完，完整参考答案为learning_output/cases/2023-A-transfer/revision_v9/REFERENCE_SOLUTION.md，汇总为同目录LEARNING_SYNTHESIS_10_PAPERS.md。下一步做新题先答后对照的迁移检验。作者完整程序复现0篇，正式Core v1.41.0不变。只在本地，不处理GitHub、不解析PDF。下方旧进度为历史记录，以PROJECT_STATE.json为准。

> 最新状态（2026-09-22）：2023-A已完成6/10篇全文文本评审，完整参考答案为learning_output/cases/2023-A-transfer/revision_v8/REFERENCE_SOLUTION.md；第六篇A23102890028已完成。下一篇A23103360079（77页），文件已在本地。原作者完整程序复现0篇，正式Core仍v1.41.0。只做本地学习，不处理GitHub、不解析PDF。下方较早状态仅作历史记录，以PROJECT_STATE.json和最新进度为准。

> 最新本地状态：5/10篇全文评审；第六篇A23102890028部分评审及标定检查完成。完整主解仍revision_v7，新增CALIBRATION_SUPPLEMENT.md。下一步读完第六篇；仅本地工作。

# 新 Chat 接续说明

更新于 2026-09-22，第二篇收尾完成之后。先读本文件，再读 PROJECT_STATE.json；历史对话中的“第二篇未收尾”已被此次实际文件更新取代。

仓库实际项目根目录为 `current/`。本说明中相对文件路径均相对于 `current/`；仓库根 README 指向这里。

## 我们在做什么

用户要让 Skill 学习优秀数模论文的选模、推导、代码、验证和写作，再对新题生成完整参考解答，供自己对照改进作品，以提高竞赛能力。用户目前没有指定练习题和自己的答案，已经授权自主选题、整理资料并继续学习。不要用不断整理版本和角色比较替代真实论文学习。

这是知识、案例和工作流程的学习，不是对基础模型进行参数微调。正式 Core 仍为 v1.41，本仓库是工作副本；没有获奖率提升证据。Architect/Reviewer 是实验接口，完整多 Agent 生产流程未部署。

## 必读文件及当前状态

1. PROJECT_STATE.json、START_HERE.md。
2. .agents/skills/graduate-mathmodel-learning/SKILL.md 及对应 paper-review、code-paper-figure-learning、delivery-learning-local 等说明。
3. learning_output/context/next_learning.md。
4. learning_output/cases/2023-A-transfer/PAPER_REVIEW_PROGRESS.md 与 PAPER_MARKDOWN_REGISTRY.json。
5. 当前完整解答 learning_output/cases/2023-A-transfer/revision_v3/REFERENCE_SOLUTION.md。

2022-C v3 已交付，不重跑。2023-A 学习前的四问答案、16 个主场景及敏感性实验已冻结；ZIP 位于 learning_output/cases/2023A_first_answer_v1_frozen.zip，SHA256 为 be43296f76ee37d241ed5314514a009fc945aa3d98b9966c8d3facf7b513d24f。FIRST_ANSWER_FREEZE.json 内含文件哈希。禁止覆盖原冻结产物。

第一篇 A23104220005（49 页）已完成全文文本评审、20 次局部调度探针和 20 条连续轨迹诊断；成果在 paper_learning/A23104220005 和 revision_v2。

第二篇 A23100070049（56 页）已完成全文文本评审、四种干扰情形共 20 次仿真及四条短轨迹验证，评审和知识沉淀已经收尾；成果在 paper_learning/A23100070049 与 revision_v3。不得重跑它来代替下一篇学习。

两篇都没有完整执行原作者 MATLAB，原图像素也未核验。2/10 指全文文本评审完成，不是全流程复现，更不是把正式库的 45 篇改成 47 篇。

## 已学到并改进了什么

第一篇带来连续每秒逐节点分布与计数守恒验证。第二篇补足 Q4 相邻干扰关系未明确时的四种条件化答案，并验证 Q2 不能漏掉双发双成功收益。

Q4 的 5 秒观测实验（每组 5 种子）总均值：两边干扰 110.83104；仅 1–2 干扰 113.45568；仅 2–3 干扰 113.50368；均不干扰 117.08496 Mbps。参数、区间与验证范围见 CHECKS.json 和修订解答。这些是双向对称干扰假设下的结果，不覆盖所有物理情形。

## 下一步怎么做

下一篇是 **A23102470073**，路径 `learning_sources/2023A_markdown/A23102470073/`。逐页读 Markdown，按 Q1–Q4 与前两篇横向比较，优先检查 Q3 隐藏节点脆弱时间的解析推导和 Q4 拓扑、冻结与解冻时序。

每问记录作者模型、输入、关键公式、代码映射、结果、验证、可采纳优点与限制。选择能改变当前解答的具体改进，进行最小但有意义的运行验证，再保存独立修订。不要为了贴合论文数字而修改模型；作者主张、静态发现、我们的实验和完整复现必须分开。

每篇完成后更新状态、进度与知识卡，保留前后差异。公式不清楚先看同目录 raw_layout；仍缺时记录论文、物理页及公式编号，必要时让用户补 Markdown。**绝不直接解析 PDF。**当前已具备其余 8 篇 Markdown，无需等待用户提供自己的答案。

## 网页版怎么取得文件

仓库中已加入 10 篇正文及 10 份 raw_layout，登记表优先使用 `*_repo_path` 相对项目根目录（仓库的 current/）解析。原 Windows 绝对路径仅为来源记录；不要尝试在网页环境访问用户 D 盘。图片未复制，原论文图片回退链接不能使用。

网页普通访问曾返回 404，但本机 Git 可以认证读取远端。新 Chat 必须有仓库访问权限，或者由用户上传仓库 ZIP；一个链接不保证所有网页工具均能访问私有仓库。无需为此将仓库改为公开。

如果上传文件：优先整个仓库 ZIP。最小接续集合为本说明、项目状态、Core 技能及引用文件、knowledge_base、2023-A 案例完整目录、冻结 ZIP 和 learning_sources/2023A_markdown；缺任何关键目录时请先明确缺口，不能声称已读取。

## 对话记录与复算

本地会话可见用户/助手消息导出见 CONVERSATION_EXPORT.md。它排除系统/开发者消息、工具输出与内部推理，只记录本地日志现存文本；引用的两个旧 ChatGPT 会话全文不在该导出范围。该记录用于理解历史，最新文件状态优先。

Python 代码以标准库为主，运行位置不应依赖 Windows 路径。一般无需重跑已完成的几十组仿真；先检查保存结果与哈希。源码和 README 的复算入口仍可使用。没有条件运行时如实记录，不能补写 PASS。
