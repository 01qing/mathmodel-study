from pathlib import Path
import sys,json,importlib.util
OUT=Path(__file__).parent
sys.path.insert(0,str(OUT/'runtime_deps'))
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(r'D:\softdown\codex\mathmodel-study\current')
path=ROOT/'.agents/skills/mathmodel-case-retriever/scripts/search_cases.py'
spec=importlib.util.spec_from_file_location('search_cases',path); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
queries={
'A':'有向无环图多核调度 任务依赖 资源容量 缓存 数据搬运 事件仿真 最大完成时间 优化与独立约束校验',
'B':'燃料电池 传热传质 相变结冰 一维瞬态偏微分方程 参数标定 留出验证 动态控制 能耗优化',
'C':'脑电信号 时间序列 去噪 事件相关电位 神经动力学模型 参数可辨识性 分类 交叉验证',
'D':'无人机应急物资运输 路径调度 载重电池时间窗 连续通信遮挡 链路预算 中继资源分配 独立可行性验证',
'E':'多模态文本语音视觉 特征时序对齐 缺失信息 情感分类 回归 可解释性 消融 验证集 标签泄漏',
'F':'多来源数据 质量评价 配比单纯形 非线性回归 标度律 参数辨识 资源预算约束 多目标优化 外推不确定性 因果识别'}
results={}
for letter,q in queries.items():
    r=module.search(q,'production',3); results[letter]=r
    print(letter,[(m['paper_id'],m['case_group'],m['page'],m['title']) for m in r['matches']])
(OUT/'training_retrieval.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
papers=json.loads((ROOT/'.agents/skills/mathmodel-case-retriever/assets/papers.json').read_text(encoding='utf-8'))
(OUT/'training_catalog.json').write_text(json.dumps([{k:p.get(k) for k in ['paper_id','case_group','paper_title','title','split','learning_status','review_file','reviewed_pages']} for p in papers],ensure_ascii=False,indent=2),encoding='utf-8')
