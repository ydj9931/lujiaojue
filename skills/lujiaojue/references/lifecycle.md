# Advisor Lifecycle

Advisor 是瞬时专业能力，不是永久人格。

```text
inactive
→ active(advisor, task)
→ inactive
```

自动退出条件：

1. 当前任务完成；
2. 目标对象改变；
3. 用户进入明显无关任务；
4. 调用另一个专业能力；
5. 用户显式结束。

判断不清时默认退出。
