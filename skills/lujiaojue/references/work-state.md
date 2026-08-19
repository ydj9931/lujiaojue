# Work State

鹿角蕨真正的核心是 Work State，不是 HTML 页面。

扫描脚本只能提供证据，以下五项必须由宿主 Agent 基于关键文件、明确事实和用户上下文判断：

```text
final_outcome      最终成果
key_time           最近关键时间
current_focus      当前最重要
pending_decision   当前待决策
risk               当前最大风险
```

写入：

```text
.lujiaojue/workspace.json
→ work_state
```

原则：

- 没有证据就留空；
- 不从文件夹名字猜“最终成果”；
- 不从最近修改时间猜“当前最重要”；
- 不制造虚假截止时间；
- 待决策必须是真正阻塞后续行动的决定；
- 风险只保留最影响成果或关键节点的一项。

每日简报和工作台都优先读取 Work State。
