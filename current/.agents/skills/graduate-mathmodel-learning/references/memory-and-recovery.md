# Learning Memory And Recovery

## 两套记忆

### 正式工作流记忆
原版：
`paper_output/context/workflow_memory.json`

表示：
“这道正式赛题做到 S 几”。

### 学习状态
本 Skill：
`learning_output/context/learning_state.json`

表示：
“学习者掌握到什么程度”。

## 掌握等级

`unseen`
未系统接触。

`introduced`
知道方法是什么。

`can_explain`
能解释核心思想、假设、适用和不适用条件。

`can_apply_with_help`
在提示下能完成建模。

`can_apply_independently`
必须存在独立做题/训练证据，不能仅因看懂答案升级。

`can_compare_and_adapt`
能比较替代方法、指出切换条件并改造模型。

## 新对话恢复
优先读取文件，不凭聊天历史猜测：
1. learning_state
2. next_learning
3. 最近 session
4. 若正式比赛并行，再读原 workflow memory
