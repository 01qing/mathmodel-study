# S014 Dev 候选规则（尚未发布进稳定Core）

来源仅S014 Dev及本地数学/代码审计。Test比较内容未用于本增量。与v1.39数据合同规则去重后，拟扩展以下具体检查：

1. 扩展既有时间支持门禁：多级mean须保留有效样本数，mean-of-means不默认等于整体mean；年度累计、日均、面积加权分别命名。
2. 扩展既有实体/轴门禁：flatten后的统计量、布尔mask与输出栅格登记相同顺序及shape；矩阵计算、权重连接和输出表均保留indicator_id。
3. 扩展既有实际primitive审计：AHP主特征向量、几何均值、列归一化均值不得混称；A、w、lambda、CI、RI(n)、CR逐项重放，数值近似不能自动认作同一算法。
4. 扩展既有变量/单位门禁：循环变量重采样先处理周期；地理对齐登记crs/transform/extent/resolution/nodata，禁止只查数组大小。事件率同时登记有效暴露分母。
5. 扩展既有Result Registry：跨模型比较必须同target及heldout entity_id集合；真实Y条件只能用于事后诊断，不能成为未知Y时的模型路由规则；统计显著与预测增益分开。
6. 扩展既有组合门禁：分层权重按键传播，乘积与加权和保存不同operator_id；组成数据输出必须满足声明的总量及边界（五类不完备时加other或声明≤1）。

不另建同义规则或角色Skill。尚未修改稳定Core，也未把Dev卡片加入Train检索。候选代码为audit_replay.py中的局部函数；不是生产就绪地理分析库。审核这些扩展与现有长期规则的重叠后，再决定v1.40最终最小增量。

不得纳入通用规则的内容：作者60–90degree等具体阈值、AHP数值、地名风险判断和未来地图。不得因本地合同测试通过而声称clean blind Core gain。题组Mini Transfer在S015/S016完成后追加。
