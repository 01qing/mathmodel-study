# 2023-A 案例修订 v2

REFERENCE_SOLUTION.md 是完整参考解答，末尾追加第一篇优秀论文带来的验证改进。不是新 Core 发布，不覆盖学习前冻结包。

复算：用 Python 3 运行 `../paper_learning/A23104220005/run_learning_checks.py`（标准库，无新增依赖），再运行同目录 `save_learning.py`。前者调用冻结版 code/wlan.py，运行 20 个调度探针及 20 条连续仿真轨迹，后者验证冻结文件和来源哈希后生成本目录。

原四问主计算入口和参数见 ../code/run_experiment.py；本修订不需要重跑全部主场景。所有新增每秒数据在 ../paper_learning/A23104220005/LEARNING_CHECKS.json。作者 MATLAB 未执行，局部 Python 探针不得称为原作者完整复现。
