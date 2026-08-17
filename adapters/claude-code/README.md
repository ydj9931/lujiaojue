# Claude Code

本仓库根目录已经包含：

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
skills/
```

## 本地测试

```bash
claude --plugin-dir ./lujiaojue
```

## GitHub Marketplace 安装

仓库推送至 `ydj9931/lujiaojue` 后：

```text
/plugin marketplace add ydj9931/lujiaojue
/plugin install lujiaojue@lujiaojue
```

安装后，Plugin 中包含：

- `lujiaojue`
- `fuli`
- `xiaowang`

三个 Skills。
