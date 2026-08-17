# Architecture

```text
Host Agent
   ↓
Installation Layer
Plugin / Skill / Marketplace
   ↓
skills/
├── lujiaojue  → Workspace + Router + Workbench
├── fuli       → Compounding Creation Advisor
└── xiaowang   → Project Advisor
```

三层职责：

```text
Plugin / Extension = 安装与分发
Skills             = 判断与能力
HTML               = 当前工作台显示方式
```

HTML 不承担路由、状态或 Advisor 判断。

Advisor 版本独立：

```text
Lujiaojue 0.2.0
Fuli      0.5.0
Xiaowang  0.4.0
```
