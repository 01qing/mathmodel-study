# 安装到 MathModel-Skill / Codex 项目

## 方式 A：已经有一个 MathModel-Skill Codex 项目

把：

```text
.agents/skills/graduate-mathmodel-learning/
```

整个文件夹复制到项目的：

```text
.agents/skills/
```

最终与原 10 个 Skill 并列。

然后在项目根目录运行：

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/init_learning_workspace.py
python .agents/skills/graduate-mathmodel-learning/scripts/validate_learning_workspace.py
```

## 方式 B：修改 yushui2022/MathModel-Skill 源仓库的 Codex package

把该 Skill 文件夹复制到：

```text
packages/codex/.agents/skills/graduate-mathmodel-learning/
```

不要覆盖原 10 个 Skill。

## 首次检查

```bash
python .agents/skills/graduate-mathmodel-learning/scripts/route_mode.py --mode learn
python .agents/skills/graduate-mathmodel-learning/scripts/route_mode.py --mode competition
```

competition 模式必须检测到原 `paper-workflow-orchestrator`。
