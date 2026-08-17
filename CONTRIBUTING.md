# Contributing

鹿角蕨欢迎来自真实工作场景的贡献。

## 最优先的贡献

1. **真实问题**：什么地方让用户困惑、增加操作负担或产生误判。
2. **测试案例**：能够稳定复现 Advisor 判断问题的最小案例。
3. **Advisor 改进**：只修改真正属于该 Advisor 的能力。
4. **适配改进**：让更多 Agent 可以更自然地安装与调用鹿角蕨。

## Advisor First

升级富丽：

```text
默认修改 skills/fuli/
```

升级小王：

```text
默认修改 skills/xiaowang/
```

升级鹿角蕨工作空间 / Router / 工作台：

```text
默认修改 skills/lujiaojue/
```

只有稳定、明确的跨 Advisor 公共能力，才上移为公共协议。

## 新 Advisor 的门槛

不要因为“可以做”就创建新 Advisor。

至少满足：

1. 问题在真实工作中反复出现；
2. 需要稳定的专业判断；
3. 普通 Agent 临时处理效果明显不足；
4. 已有多个真实场景支持；
5. 有办法验证它是否真的提高结果质量。

## 提交建议

Commit 示例：

```text
feat(lujiaojue): improve workspace object detection
feat(fuli): add publication tracking
feat(xiaowang): add project drift checks
fix(router): prevent advisor context leakage
```

请优先提交小而清晰的改动。
