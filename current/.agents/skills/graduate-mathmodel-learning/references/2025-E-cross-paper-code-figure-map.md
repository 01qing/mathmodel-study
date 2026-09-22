# 2025 E：三篇优秀论文 × 补充代码 × 图表论证映射

> 边界：S039/S040/S041 是优秀论文训练样本；GTeacher1/GTeacher2 是教师/专家补充材料。方法相似不代表代码属于论文作者。

## Q1 数据与特征

- **S039**：轻量路线。窗口扩样后做 39→14 特征筛选；相关性、PCA、RF 重要性、互信息/卡方构成筛选证据链。
- **S040**：强噪声路线。48k→32k，TVFEMD+GWO-MOMEDA 去噪，SMOTE，36 特征+MixHop。
- **S041**：机理筛样路线。32k，1024/512 滑窗，SNR/RMS/crest 筛样并保留 10% 低分样本，手工特征+ViT 特征。
- **GTeacher1**：MAT→CSV、小波/EMD，适合作为最小信号探索基线。
- **GTeacher2**：detrend、bandpass、Hilbert envelope、resample、window、谱峭度、阶次跟踪，更接近批处理实现。

**切换规则**：先看故障特征频率和包络谱是否已清晰；若简单滤波足够，不要为了“高级”强行上复杂分解。任何滑窗都先按原始文件/工况分组，再切窗。

## Q2 源域分类

- S039：SVM/RF/MLP 与 VGG/CNN；五折。
- S040：RF/LSTM/CNN/ViT；加入 10 次箱线图评价稳定性。
- S041：KNN/TCN/DenseNet/ResNet-CBAM；比较 6:4/7:3/8:2。
- GTeacher1 RF 可做最小基线；GTeacher2 的 1D 网络、机理滤波组和文件级划分可作较完整代码骨架。

**强制检查**：分层随机切分并不等于防泄漏。来自同一原始振动记录的重叠窗口必须保持在同一 split。

## Q3 无标签目标域迁移

- S039：CNN + 边界/分布对齐，MMD+CORAL/DDM。
- S040：KDE 先证明域偏移，再做 ViT + 高阶/二阶联合矩匹配。
- S041：源统计 Z-score + DANN+MMD + 聚类/伪标签。
- GTeacher2：可直接借鉴 CORAL、entropy minimization、BN 适配、目标文件聚合和两次预测融合的代码阶段。

**最小实验阶梯**：源模型直接目标推理 → +CORAL/MMD → 必要时 +DANN/伪标签。每升级一层都保留上一层作消融。

## Q4 可解释性

- S039：域级解释，MMD/CORAL/DDM+t-SNE。
- S040：域前后嵌入、距离/质心方差、attention。
- S041：事前结构/机理 + 迁移过程 + SHAP 事后解释，层次最完整。
- GTeacher2：embedding、gate/channel 权重、包络样例、adapt loss、融合置信度可补代码实现。

**证据边界**：t-SNE 混合不是准确率；attention/SHAP 不是因果证明；目标域置信度不是目标域真值性能。

## 图表顺序模板

1. 数据/物理机理是否合理。
2. 为什么需要特征筛选或去噪。
3. 模型竞争与稳定性。
4. 为什么需要迁移（源/目标域差异）。
5. 迁移训练是否真的降低域差异。
6. 目标结果与不确定性。
7. 迁移前/中/后的解释。

图的数量不固定。每张图必须先写 `purpose` 与 `cannot_prove`，只有存在证据缺口才画。
