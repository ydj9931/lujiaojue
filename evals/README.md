# Evals

鹿角蕨 v0.3 测试优先级：

```text
减熵误判
→ 模式误判
→ 成果偏航
→ 复利过度
→ Advisor 生命周期
```

- `core/`：鹿角蕨初始化、减熵信号、工作台、Router。
- `fuli/`：复利判断。
- `xiaowang/`：成果与项目判断。
- `install/`：宿主安装发现。

修改鹿角蕨主 Skill 时至少运行 core eval。
修改 Advisor 时默认只运行对应 Advisor eval；涉及路由或生命周期时增加 core eval。
