# v1.21 Validation

- S017 专项测试：60/60 PASS。
- S017 检索回归：PASS。
- 历史检索：2024-A S003/S004、2024-B S005-S008、2024-C S009-S012 已逐项复跑通过。
- 库存逻辑：45 papers / 6752 chunks / 32 train / 7 dev / 6 test。
- reviewed 边界：train S001-S012、S017；dev=[]；test=[]；S018-S020 仍未吸收。
- frozen split manifest SHA256 与记录一致：`0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`。
- 限制：当前工作区没有原 D 盘 45 个 PDF，因此本轮不重新逐字节计算原 PDF 哈希；沿用此前已冻结的 PDF 身份/page inventory，并验证当前 papers/split registry 未改变。S017 当前无作者完整运行工程与全部外部模型/视频依赖，故不声称端到端复现。
