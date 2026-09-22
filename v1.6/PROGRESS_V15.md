# v1.5 Progress

## 本轮最重要的修正

2024 C 不能再称 fresh blind。

因为在候选模型矩阵冻结之前，已经读取过：
- 公开 Q1/Q2/Q4/Q5 代码
- 数模之星冠军方案简介
- 其他获奖方案简介

因此本轮正式记录：
`RETROSPECTIVE_INDEPENDENT_ROUTE_NOT_FRESH_BLIND`

这是学习系统必须记录的“证据暴露顺序”。

## 独立模型竞争矩阵已完成

### Q1
主线：
`原始波形 -> 形状/斜率/频域特征 -> RF/SVM`

1D CNN 只在跨工况验证确有收益时升级。

### Q2
主线：
`Steinmetz -> log-domain温度修正 -> leave-one-temperature-out`

优先简单可辨识模型，不按训练SSE选最复杂模型。

### Q3
主线：
`log P ~ log f + log Bm + T + W + M + 两两交互`

配合 HC3 稳健误差与效应量。

### Q4
主线：
`物理基线 + Ridge + RF/ExtraTrees + boosting`

必须同时报告：
- 随机/分层CV
- 跨温度/材料/波形工况诊断

### Q5
目标显式为：
- `min predicted loss`
- `max f*Bm`

简单基线：
`枚举离散组 + LHS/密集采样 + Pareto筛选`

主候选：
`NSGA-II`

替代：
`epsilon-constraint`

## 优秀论文入口

已经核实：
- `zhanwen/MathModel` README 提供 2024优秀论文合集
- 百度云入口存在
- 提取码 `opr4`

当前运行环境无法访问百度网盘，因此：
`full papers materialized = 0`

不能声称两篇全文已读。

## 新增 Blind Gate

以后第三个、第四个案例必须：
1. 只看题面与官方附件
2. start_blind_case
3. 冻结独立矩阵
4. 再读论文/代码

## 下一步

最优先不是继续改2024 C规则，而是：
- 如果后续能取得2024全文：直接做论文A/B vs 独立矩阵；
- 如果仍不能取得：进入一个从未看过解法的第三案例，用新blind gate做第一次真正无污染测试。
