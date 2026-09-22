# 2024-C S012 论文—代码联合审计

## 范围
- 论文：S012 / C24106130096，共105个物理页。
- 状态：全文精读 + 打印附录静态审计 + Q1/Q5 exact contract replay。
- 未宣称：缺官方附件/完整派生特征与模型检查点，因此未做作者全链端到端复现；当前工作树没有原PDF像素级排版审计。

## Q1
路线为形状阈值→5维统计特征SVM→噪声压力测试→Hilbert-Huang+双谱多域特征。可学习的是“先发现简单表征在噪声下失效，再扩展表征”的论证链。打印代码中，`get_feature()` 对完整特征矩阵先计算feature-wise min/max，再进入 `get_res()` 做 train_test_split；`data_10`/`data_snr_10` 也在 split 前按列缩放，因此验证集极值参与训练预处理。新实现必须 split/group first，所有跨样本 scaler 只 fit train fold。

## Q2
SE→LSE→TLSE→TLSEDSR 是很好的物理到自适应模型梯子；打印代码能看到真实 NAdam/网络路径。问题在于主证据仍是同一材料/波形支持内的随机80/20行切分。`R2≈1/MRE≈0.12` 只能称插值性能；跨温度/材料泛化需 leave-condition-out。

## Q3
优点：S012 真正写出三因素模型与两两 interaction term，强于只画交叉均值图。风险：表5.19正文把截距F=3456.213错写成温度F，温度行实际F=17.755；随后又把不同one-way ANOVA的F直接作为“影响程度”排序。F不是跨模型可直接比较的效应量，应报告partial eta²/omega²或统一调整模型中的contrast。47次Mann-Whitney序贯淘汰未见多重比较校正，而且算法对组顺序敏感。

## Q4
DM/DMSDR/TDM/LMSE/LMSESDR/TLMSESDR/MTLMSESDR/WMTLMSEDSR 形成完整ablation ladder；打印代码存在材料和波形Embedding，最终WMTLMSEDSR的实现证据比S010/S011更完整。仍要注意所有高分基本来自随机行切分；跨材料/温度/波形/频率区间的真正泛化应使用grouped/leave-condition-out折。

## Q5 exact replay
论文明确 `50000<=f<=500000`，GA/PSO打印代码却均使用 `lb=[5000,...]`。因此论文报告的PSO `f=7862.85` 在代码域内可行、在论文模型域内不可行。温度理论上只能取 `{25,50,70,90}`，材料/波形为离散类别，但优化器接受连续坐标。

按论文公式 `L=P_loss-lambda*energy` 复算表5.37/5.38：lambda=0.01/0.1/1 与表一致；标为lambda=10的行实际隐含lambda≈100，标为lambda=100的行实际隐含lambda≈10，说明结果行/标签存在漂移。打印脚本 `Lambda=[0.01,0.1,1,10,100][4]` 只选择100，不能在一次未改代码运行中产生整张lambda扫描表。

## 新题迁移
可借鉴：物理基线→逐步修正→深度自表示的假设梯子；显式interaction；Q4逐步ablation。
不得照搬：split前缩放、随机行泛化、F统计量当效应量、未校正47次检验、连续松弛离散决策、纸面/代码边界分叉、无法replay的lambda表。
