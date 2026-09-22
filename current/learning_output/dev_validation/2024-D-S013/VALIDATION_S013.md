# S013 结案验证

日期：2026-09-12。主结果文件：validation/S013_CLOSURE_VALIDATION.json。

42/42结案检查通过：页码覆盖/来源hash、四问schema、竞争方案、结果证据引用、矛盾保留、必要算术一致性、专项记录、七门不越界、冻结Core与答案、split和chunk数量。不是作者模型正确性或能力增益测试。

专项4个程序均退出0，日志为 validation/audit_*.log。部分程序输出是矛盾、未解决或条件反例，不能把退出0解释为论文结果全部通过。

历史原样21/22通过，额外v1.38原样失败。原因及外部适配精确文本在 validation/COMPATIBILITY_RETEST.json 和 *.external-adaptation.txt；两项适配复测通过，v1.38为127/127。原始失败日志不覆盖、不删除。run_revalidation.py 的全通过断言因此以非零退出，这是保留的真实原始结果；retest_compatibility.py 和 validate_s013_closure.py 则验证适配状态及闭环范围。

retrieval smoke实际执行退出0，见 validation/retrieval_smoke.log。其结果限定 reviewed-Train-only；未将S013加入Train检索。split保护验证的是冻结元数据和字节，不是对历史上“从未接触答案”的证明。

冻结保护：Core1470/1470未变；独立解答55/55未变；manifest SHA256 `ee139e2a7063fd6cb3a279ae5acba633f2e6784f8afa62d9e51fbc9a1db42a7e`。S013源PDF SHA256 `a8c55b50f7be97971dc0b5844952dcbdc6929c07f52f841c0d0add83bec7628d`。

复现等级R2；视觉113/113单独记录。作者中间表、可运行源工程和GIS链仍缺失。不声称R3+、R7、clean blind gain或Core v1.39 SEALED。
