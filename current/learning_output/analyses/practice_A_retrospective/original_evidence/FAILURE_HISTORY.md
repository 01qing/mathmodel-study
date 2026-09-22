# 本轮失败与修复

1. 通用路线生成器不能识别英文mechanistic_simulation类型，产生泛化“可解释模型”。人工核对后用已审题的径向PDE路线替换，保留model_route_initial_generic.json；未修改Core。
2. 图表计划生成器控制台在GBK环境输出勾号失败。重新以UTF-8运行成功；此失败不是数据不可读。
3. 数据计划生成器将result模板列入计划。按输入manifest与题面将4个模板移至excluded_result_templates，只允许附件1/2作为模型输入；实际加载器本来就跳过模板。
4. 捆绑Python缺scipy，第一次数值启动失败。用捆绑环境只读提取XLSX为CSV，数值计算使用已具备scipy的Python，避免修改依赖或Core。
5. 均匀网格含水率收敛FAIL。保留q1_FIRST_FAIL_uniform_grid.json与q1_uniform_grid_first.py；诊断早期表面边界层，改表面加密网格后通过原阈值。只通过数值基线检查，真实物理准确度未建立。
