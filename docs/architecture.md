# Architecture

鹿角蕨 v0.5 的核心不再是 HTML Workbench，而是：

```text
Host Agent
   ↓
小鹿
   ├── Work State
   ├── Daily Brief
   ├── Context
   ├── Router
   ├── Advisors
   │   ├── Xiaowang
   │   └── Fuli
   └── Views
       └── Workbench
```

## 用户层

```text
小鹿启动
小鹿开工
小鹿，……
小鹿工作台
```

## Work State

真正的工作台首先是一份持续更新的工作状态：

- 最终成果；
- 关键时间；
- 当前最重要；
- 待决策；
- 风险；
- 当前事实源；
- 文件熵；
- 重复结构；
- 长期成果。

## Daily Brief

每天第一次进入工作文件夹：

```text
轻量刷新
→ 状态
→ 下一步建议
→ 待决策
→ 风险
→ 提醒
```

最多 5 个认知块。

## Workbench View

HTML 只是辅助视图。

默认桌面提供「小鹿工作台」入口，但状态仍保存在工作文件夹中。

工作台第一屏只呈现：

```text
最终成果
关键时间
当前最重要
待决策
最大风险
```

不解释功能。
