# S013 Dev 调优候选：最终登记，尚未合并 Core

本轮复用唯一 MathModel-Core。冻结 v1.38 的 Skill 文件保持不变；不把 Dev 论文、阈值、结论写入 Train 检索。以下候选先与已有规则去重，再进入下一次明确版本化的调优。

已有规则应增加反例而非重复扩写：

- v1.13“先定义独立样本单位再切分”、v1.18“泛化单位”：补充 entity-time 多对多合并和三行/三年窗口反例。新增的是可执行前后行数、唯一键和日期窗口断言。
- v1.17 特征 schema、v1.18 变换 schema：补充文件选择器只能选到 Jan1 时禁止输出“年均”；同年全国输入不能无来源生成地区差异。
- v1.18 类别 vocabulary：补充绘图名称从 encoder/model.classes_ 派生，且审计必须按代码分支，不能把字符串分支的问题外推到数值分支。
- 既有 Result Registry、量纲及实际 primitive 审计：补充 importance_type=weight/gain、目标=降水/易损性、统计量=SVR/Gi*/LocalMoran、run_id 和数据版本。指标不同先判不可比较，不自动判数值错误。

适合作为新专门合同候选的内容：

- 自构指数标签与独立真实结果必须分栏；伪标签精度只评价指数模仿。已有标签/代理指标规则需继续全库去重后决定是否新增章节。
- 分布摘要与总量分账：sum(area×fraction) 是资源量，协方差椭圆描述空间离散；权重整体翻倍应改变总量，不应改变归一化协方差。
- 椭圆概率覆盖声明必须给维数、尺度、分布前提及外部覆盖验证。描述协方差不必强加正态假设，coverage_ratio 的一维 KDE 不能验证空间坐标联合正态。
- 模型名称、实现分支、训练输入、未来输入、输出图必须串成可追溯运行链；缺失部分保留 UNVERIFIED，不用相似图补位。

局部反例与修复证据见 COUNTEREXAMPLE_RESULTS.json、SPATIAL_PROVENANCE_RESULTS.json、FINAL_PRIMITIVE_RESULTS.json。它们支持机制诊断，不证明集成后有独立收益。下一版仍需解释稳定性及下游效用实验；本轮没有把这些未运行项目标成 PASS。
