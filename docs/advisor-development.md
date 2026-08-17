# Advisor 独立升级规范

## 原则

> **Advisor First：专业能力优先在所属 Advisor 内独立演化。**

版本不绑定：

```text
鹿角蕨 0.1.0
├── 富丽 0.5.0
└── 小王 0.4.0
```

## 升级小王

推荐短期分支：

```bash
git checkout -b advisor/xiaowang-v0.5
```

默认允许修改：

```text
skills/xiaowang/
evals/xiaowang/
```

默认不修改：

```text
skills/fuli/
core/
SKILL.md
```

完成后：

1. 修改 `skills/xiaowang/VERSION`；
2. 更新 `skills/xiaowang/CHANGELOG.md`；
3. 运行小王 eval；
4. Commit；
5. Merge main；
6. Tag。

建议：

```bash
git commit -m "feat(xiaowang): add project drift detection"
git tag xiaowang-v0.5.0
```

## 升级富丽

同理：

```bash
git checkout -b advisor/fuli-v0.6
git commit -m "feat(fuli): add publication tracking"
git tag fuli-v0.6.0
```

## 什么情况下改 Core

只有能力已经被证明是稳定的公共需求时：

- 生命周期；
- 工作空间读取；
- Router；
- 公共状态协议；
- Advisor 注册机制。

不要因为两个 Advisor “可能都能用到”就提前抽象。

## 鹿角蕨版本何时升级

主要涉及：

- 初始化方式；
- 工作台；
- Router；
- 生命周期；
- `.lujiaojue/` schema；
- 安装 / 更新机制；
- Core 公共行为。

单个 Advisor 升级不要求鹿角蕨同步升级版本。
