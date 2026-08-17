# UI

v0.1 不建设独立桌面 App。

当前工作台由：

```bash
python scripts/render_workbench.py /path/to/workspace
```

生成到用户工作目录：

```text
.lujiaojue/workbench.html
```

第一版界面只优先回答：

1. 我最近在做什么？
2. 什么发生了变化？
3. 什么值得我关注？

未来 UI 应由工作模型生长，而不是先做一个固定 Dashboard 再要求用户迁就。
