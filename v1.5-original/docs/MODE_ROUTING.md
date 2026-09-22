# 五种模式路由规范

## 1. learn

### 目标
系统学习一套研赛题或某一问。

### 读取
- 原题与附件
- `problem_analysis.json`（若已存在）
- `model_route.json`（若已存在）
- 优秀论文/专家答疑/代码
- `learning_state.json`

### 允许调用原版
- `problem-doc-model-selector`
- `modeling-paper-rubric-and-model-selector`
- `data-cleaning-and-visualization`
- `model-code-and-result-generator`
- `quality-assurance-auditor`（只在需要正式核验时）

### 输出
- 逐问深度解析
- 候选模型比较
- 为什么选 / 为什么不选
- 公式来源与推导
- 数据→变量映射
- 求解与代码映射
- 结果解释
- 风险和失效条件
- 可迁移总结
- session record
- 学习状态更新
- 候选方法卡/题型卡

### 禁止
- 未运行代码却标记“已复现”
- 只因优秀论文使用某模型就认定其最佳
- 自动进入正式 S7/S8

---

## 2. competition

### 目标
正式完成赛题与论文。

### 最高入口
`paper-workflow-orchestrator`

### 路由
严格 S0-S8。

### 学习扩展作用
只做旁路解释：
- 为什么当前 S2 选择该路线
- 关键风险
- 赛后待复盘点

### 禁止
学习扩展不得绕过 workflow guard，不得自行写正式 evidence PASS。

---

## 3. paper-review

### 目标
精读一篇或多篇优秀论文。

### 读取
- 原题
- 论文
- 附件
- 代码（若有）
- 相关官方答疑/学术论文

### 输出
逐问记录：
- 作者做法
- 作者主张
- 证据位置
- 模型假设
- 数据处理
- 数学模型
- 求解
- 验证
- 优点
- 风险
- 可疑点
- 我们的核验状态
- 我们的改进建议

### 多论文比较
比较同一问题，不做“整篇论文笼统优劣”。

### 证据状态
`author_claim | verified | partially_verified | not_verified | contradicted | our_inference`

---

## 4. review

### 目标
对已经学过/做过的赛题进行复盘。

### 输出
- 哪些判断正确
- 哪些路线浪费时间
- 哪些假设最危险
- 哪些验证不足
- 哪些代码问题具有模式性
- 下次遇到相似题的识别规则
- 更新 error pattern / competition lesson

### 关键要求
复盘不是重新写解答，而是抽取决策经验。

---

## 5. practice

### 目标
训练用户独立建模。

### 默认过程
1. 只展示必要题目信息。
2. 要求学习者先提交：
   - 问题类型
   - 变量/目标/约束
   - 候选模型
   - 推荐路线
   - 验证方案
3. 再比较：
   - 学习者方案
   - 优秀论文方案
   - 原版 S2 路线（若有）
   - 我们的综合判断
4. 只在反馈阶段展示标准思路。

### 评分维度
- 问题结构识别
- 变量映射
- 模型适配
- 替代方案判断
- 验证意识
- 风险意识
- 表达清晰度

### 学习状态升级原则
不能因为“看懂答案”就升级到 `can_apply_independently`。
必须有独立训练证据。
