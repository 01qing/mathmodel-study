# S016 Dev 最终审查（v1.41）

S016 / 2024-D / Dev 已完成全文 114/114 页与原 PDF 视觉 114/114 页审查，打印代码 p92–114 静态审计完成，复现等级保持 **R2**。既有局部审计 **19/19 PASS**，新增视觉后续机制测试 **11/11 PASS**；这些仅验证表格算术、数学反例和接口机制，不等于作者 LSTM/RF/Gaussian/XGBoost/SHAP 全链复现。

四问 Candidate Model Competition 与 6 小时 Baseline 已完成。影响 Core 的主要通用结论包括：同名结果必须追溯 run_id 和真实输入；组成边际不能唯一识别类间流量；极端事件必须先固定上下尾、暴露单位和观测间隔；不同数组等长不等于坐标对齐；跨 CSV/程序边界必须验证 header、shape 与实体顺序；训练 loss、拟合值、OOB、随机留出、时空留出和未来地图属于不同证据；SHAP/raw margin/probability 必须声明 output_space 与 class/link；算法标题、图名和实际代码 primitive 不一致时以真实原语为证据。

关键矛盾已进入 Result Registry：正文与附录 LSTM 2015–2020 数值不一致；后两期土地 K/LUD/LUC 不满足同分母流量恒等式；部分代码重复读取错误年份；双上尾事件使用下尾 CDF 的合成反例从 0.01 被写成 0.81；RF/OLS 解释力较低且高值明显低估；混淆矩阵与 OLS 样本量不同，缺 run_id 时禁止拼接；SHAP 数值范围不支持直接概率解释；类别编码、RGB TIFF 输出与 CRS/transform 之间缺闭合链。

与冻结独立解答比较时，S016 的复杂模型数量不能作为升级依据。冻结方案保持简单可核的描述、气候态 Baseline、条件情景和结构分区；S016 中的时序、极端联合、分类和解释模块只有在同目标、同数据支持、同预算、同留出与完整输出语义下稳定增益时才允许接入。

最终状态：**S016_DEV_REVIEW_COMPLETE / R2**。作者具体参数、未来地图和未复现排行榜不进入普通 Train retrieval。
