# 2021 D Blind Baseline Protocol

## 目的

下一轮正式验收必须在“不给优秀论文内容”的条件下运行一次。

本轮负责筛选优秀论文的 Agent 已经看过论文，因此**不能把当前会话生成的独立解题结果当作真正 blind baseline**。

正确做法：
在新会话/隔离运行中，仅提供：
- 题面
- 四个数据附件
- 本 Skill
- 不提供 `paper-screening-2021-D.md`
- 不提供优秀论文 PDF

然后要求 Skill 完成以下输出。

## Q1
必须先提出至少三条合理路线，例如：
- filter：相关性/互信息
- embedded：LASSO/树模型重要性
- wrapper：RFE/顺序选择

必须讨论：
- 非线性关系
- 特征冗余
- 选择稳定性
- 20变量限制是否影响性能

## Q2
至少比较：
- 线性/PLS基线
- SVR
- 随机森林或ExtraTrees
- Gradient Boosting / XGBoost / LightGBM

禁止：
- 因为“神经网络高级”直接选神经网络
- 在测试集上反复调参

推荐验证：
- train/validation/test 或 nested CV
- MAE、RMSE、R²
- 重复交叉验证稳定性

## Q3
五个二分类标签分别检查：
- 类别比例
- 缺失
- 预测难度
- 最佳阈值

至少比较：
- Logistic Regression
- SVM
- Random Forest
- boosting family

必须报告：
- balanced accuracy
- precision / recall / F1
- ROC-AUC
- 类别极不平衡时优先 PR-AUC
- calibration（如概率要进入Q4）

采样只能在训练折内部进行。

## Q4
先回答四个结构问题，再谈算法：
1. 哪些描述符可被当作优化变量？
2. 变量之间是否存在可行域/相关结构？
3. “至少3项ADMET较好”是硬约束还是软目标？
4. 怎样保证候选描述符组合对应真实或近真实化学结构？

至少提出：
- 约束搜索/候选样本筛选基线
- 多目标优化路线
- surrogate + feasibility constraint 路线

禁止把“PSO/GA/NSGA”本身当作问题四的建模核心。

## 评分

每问 25 分：
- 结构抽象 6
- 候选模型 5
- 选择理由 5
- 验证方案 5
- 风险与切换条件 4

总分低于 80：
不得把 v0.6 升级为稳定版。
