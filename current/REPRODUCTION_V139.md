# v1.39 验证入口

从发布树根目录执行 `.agents/skills/graduate-mathmodel-learning/scripts/test_v139_contracts.py`（需numpy）验证18项局部合同；执行 `validate_v139_release.py` 验证发布不变量。历史回归入口为 `run_v139_regressions.py`，随后 `retest_v139_history.py`；原始失败与逐项版本适配分开保存。不能只运行旧版精确状态断言后据此否定新版本，也不能删除历史失败。

`learning_output/dev_validation/2024-D-S013` 是封版前原样保存的审计证据，含113页渲染和S013源PDF；其旧脚本使用最初clean-dev-2024D的路径布局，重跑真实数据审计还需原official-data及v1.39-work冻结解答目录。官方大数据集未打入本Skill包。源码级局部合同测试不需要这些外部数据。

原独立答案55文件及其manifest保持字节不变。发布中“Core当前已调优”与其中“当时Core冻结在v1.38”的历史状态不冲突。S013历史文件里的候选/NOT_SEALED不代表当前发布状态，当前以根目录RELEASE_MANIFEST_V139.json为准。
