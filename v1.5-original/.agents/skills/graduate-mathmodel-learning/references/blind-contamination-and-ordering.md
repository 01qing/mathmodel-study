# 2024 C Blind Contamination Log

## 结论

2024 C 不能再称为 fresh blind case。

在独立候选模型矩阵冻结前，已经读取过：
- Tereaslle 公开 Q1/Q2/Q4/Q5 代码；
- 数模之星冠军方案简介；
- 其他获奖队伍方案简介。

因此本轮生成的路线统一标记：

`RETROSPECTIVE_INDEPENDENT_ROUTE_NOT_FRESH_BLIND`

## 为什么这件事要写进 Skill

如果先读优秀论文，再让系统“独立推荐模型”，系统很容易把作者路线重新包装成自己的判断。

这会破坏用户真正想训练的能力：

> 不看答案时，能不能自己识别结构、提出候选、比较并做出选择？

## 下一案例的新硬门禁

首次接触新赛题：

1. 只读取题目与官方附件；
2. 写入 `solution_exposure = false`；
3. 冻结 Q1...Qn 候选模型矩阵；
4. 记录时间和 hash；
5. 然后才允许打开：
   - 优秀论文
   - 获奖方案
   - GitHub 代码
   - 博客解答

只要第3步之前已读任何解法，本案例不得再标 fresh blind。
