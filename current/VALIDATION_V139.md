# v1.39.0 发布验证

状态：SEALED。发布范围为S013 Dev审计规则增量，2024-D题组未闭环。

- 新增数据合同18/18通过；范围是局部确定性合同，不是能力增益或作者完整复现。
- 发布合同46/46通过；冻结独立解答55文件、原v1.38 Core1470文件未变；发布树只修改6个既有文件，另记录可逆中文文件名修复和4个不携带的编译缓存。
- 历史22脚本原样17/22通过；5项因S013由未读变为已评审Dev需要明确版本适配，适配后22/22。额外S045脚本也通过版本适配复测。原始FAIL、适配精确变更与适配首轮失败均保留，不能表述为“原样全部PASS”。
- 当前发布树retrieval smoke通过：evaluation/production只返回reviewed Train。45论文/6752chunks/32Train-7Dev-6Test保持，chunks和split_manifest与基线字节一致。
- Skill结构校验通过。S013=R2，视觉113/113单独记录，关键结果28条保留矛盾与未验证。

发布检查首次失败是把有意排除的4个Python缓存误判为丢失知识资产；现单独登记缓存排除，源代码/证据文件仍逐项校验。见learning_output/validation/v139/release_first_fail.json。

原S013审计中10个反例及空间/聚合记录保留FAIL→诊断→局部修复→复测，不把程序退出0等同论文数值正确。新的通用规则未改变复杂模型推荐。独立解释稳定性、下游用途、完整2024-D题组Mini Transfer和三条件Core消融尚未完成；这些不是本次单篇规则增量的发布成果。Core-level gain仍NOT_ESTABLISHED。

封版文件清单见FILES_V139.sha256和RELEASE_MANIFEST_V139.json；最终ZIP CRC与每个内容文件hash核验记录在包旁PACKAGE_VALIDATION_V139.json。官方大数据集不随Skill包重复分发，真实数据旧脚本重跑依赖见REPRODUCTION_V139.md。
