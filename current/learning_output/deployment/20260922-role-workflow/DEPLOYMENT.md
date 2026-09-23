# 数模解题与审查：本地部署完成

三个入口：mathmodel-evidence负责分流和论文学习；mathmodel-architect负责新题完整解答；mathmodel-reviewer负责有证据的审查与复核。共享同一个Core v1.41.0，默认同一助手顺序工作，未部署独立多智能体。

用户给题面Markdown和原格式数据附件后，入口执行解题→实际计算→审查→修正→复核→完整交付。无需用户自己的答案，暂不读新论文。正式比赛论文复用已有S0–S8。

已完成三个技能格式验证、八项合成数据交接检查和工作区验证，见VALIDATION.json。快照检查不能证明数学正确；尚未用真实新题完成端到端验收。

安装路径为C:/Users/lingyun/.codex/skills/下上述三个目录。协议与handoff工具在mathmodel-evidence中。旧入口和项目状态备份在本目录的.before文件。可在新会话明确调用$mathmodel-evidence；当前会话已直接读取新入口规则。不依赖后台服务或API密钥。
