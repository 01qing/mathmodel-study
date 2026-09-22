# v1.20 Validation

- S012专项测试：60/60 PASS。
- S012检索回归：PASS。
- 历史核心规则测试：v1.6、v1.8、v1.9、v1.10、v1.11、v1.12、v1.13、v1.14、v1.15、v1.16、v1.17、v1.18、v1.19、v1.20 已复跑通过。
- 历史检索：2024-A S003/S004、2024-B S005-S008、2024-C S009-S012 与 v1.9 code-link 已逐项复跑通过。
- 库存逻辑：45 papers / 6752 chunks / 32 train / 7 dev / 6 test。
- reviewed 边界：train S001-S012；dev=[]；test=[]。
- frozen split manifest SHA256 与记录一致：`0f110a9c76f1c8604dbabdee10f9c6cb701e9846755ea9577a3ef59c8318a347`。
- 限制：本轮没有重新访问原D盘45个PDF逐字节重算哈希；使用此前已核验且冻结的SHA/page inventory，并验证当前 split/paper registry 未改变。S012当前无原PDF像素级审查与官方附件端到端运行。
