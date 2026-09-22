# v1.4 Progress

## 本轮完成

1. 对 `Tereaslle/2024-CPGMCM` 进行真实代码审计
2. Q1/Q2/Q4/Q5 获得可读源码级证据
3. Q3 保持 unresolved，不根据图名猜方法
4. 新增 `2024_C_external_code_audit.json`
5. 新增 `2024_C_paper_screening.json`
6. 新增 E22-E27 真实证据型 eval
7. 新增 2024 C evidence validator

## 最重要的新发现

### Q1
- 有波形统计特征工程，值得保留
- 但顺序修改同一 dataframe 导致后续统计量混入前面派生列
- 随机70/30 holdout Accuracy=1.0，只能说明该随机切分表现极好，不能自动证明跨工况泛化

### Q2
- 最终版本保留可解释 Steinmetz 温度修正
- 但温度函数先通过边际 P-vs-T 误差筛选，存在 f/Bm 混杂
- 已检查部分的原/修正模型比较属于同数据拟合后同数据评价

### Q4
- 物理混合路线值得学习
- 缺失物理量被吸收到自由参数，预测拟合与物理可辨识性必须区分
- 已检查代码中缺少与“泛化能力”相匹配的明确跨工况验证证据

### Q5
已核验实际 objective：

`a*corrected_Steinmetz + b*loss_separation`

它只最小化磁芯损耗。

题目第二目标 `maximize f*Bm` 未进入 objective，因此当前实现没有完成题目要求的双目标优化。

## 优秀论文状态

仍为：
`NOT_YET_SELECTED`

已建立：
- 2024优秀论文外部档案索引
- 山东大学数模之星冠军 solution profile
- 江苏科技大学数模之星亚军 team profile

但没有把新闻稿冒充论文全文。

## 下一步

下一步优先级：
1. materialize 2篇完整2024 C优秀论文
2. 完成Q3代码/论文方法证据
3. fresh blind Q1-Q5 model competition
4. 论文 vs 公开代码 vs blind route 三方比较
