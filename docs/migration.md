# 从富丽与小王旧仓库迁移

源仓库：

```text
ydj9931/fuli
ydj9931/xiaowang-assistant
```

目标仓库：

```text
ydj9931/lujiaojue
```

## 原则

> **迁移当前产品，不迁移历史包袱。**

- 富丽：以 v0.5.0 为迁移基线；
- 小王：只使用 `xiaowang-assistant-v0.4/`；
- 小王 v0.1–v0.3 不复制进新仓库；
- 旧历史继续由旧 Git 仓库保存。

## 推荐迁移提交

```text
feat: initialize Lujiaojue workbench
feat: import Fuli v0.5.0
feat: import Xiaowang v0.4.0
refactor: connect advisor router
docs: add migration and advisor development rules
```

## 为什么不使用 Submodule

鹿角蕨未来需要共享：

- Lifecycle；
- Workspace；
- Router；
- 状态协议；
- 工作台。

因此使用 Monorepo。

但 Monorepo 不意味着把 Advisor 融合成一个大 Skill。

## 迁移后旧仓库

完成验证后，旧仓库可以设置为 Archived。

旧 README 顶部建议增加：

```text
本项目已并入「鹿角蕨 Lujiaojue」。
本仓库仅用于保存历史版本与开发记录。
新版本请访问 ydj9931/lujiaojue。
```

不要删除旧仓库，以保留 Git 历史和旧链接。

## 注意

本 v0.1 包已经将两位 Advisor 的当前核心规则按 Monorepo 结构整理。
如需逐字保留旧仓库的全部辅助文件，可在建立新仓后再做一次差异审查，避免把已经失效的更新脚本、旧产品说明和历史版本目录机械搬入。
