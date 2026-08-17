#!/usr/bin/env python3
"""从 .lujiaojue/workspace.json 生成一个轻量本地 HTML 工作台。"""

from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
from datetime import datetime

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>鹿角蕨 · 工作台</title>
<style>
body {{ font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; max-width:1100px; margin:0 auto; padding:40px 24px; background:#f6f6f3; color:#20231f; }}
h1 {{ margin-bottom:4px; }}
.sub {{ opacity:.65; margin-top:0; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:14px; margin-top:24px; }}
.card {{ background:white; border:1px solid #dedfd9; border-radius:14px; padding:18px; }}
.meta {{ opacity:.65; font-size:13px; line-height:1.6; }}
.badge {{ display:inline-block; border:1px solid #c8cac3; border-radius:999px; padding:3px 8px; font-size:12px; margin-top:8px; }}
footer {{ opacity:.55; margin-top:38px; font-size:13px; }}
</style>
</head>
<body>
<h1>鹿角蕨</h1>
<p class="sub">从你的工作里，长出你的工作台。</p>
<div class="grid">
{cards}
</div>
<footer>生成时间：{generated_at} · v0.1 只建立地图，不自动移动文件。</footer>
</body>
</html>
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="目标工作目录")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    state_file = workspace / ".lujiaojue" / "workspace.json"
    if not state_file.exists():
        raise SystemExit("未找到 .lujiaojue/workspace.json，请先运行 init_workspace.py")

    data = json.loads(state_file.read_text(encoding="utf-8"))
    objects = sorted(
        data.get("candidate_work_objects", []),
        key=lambda x: x.get("last_modified") or "",
        reverse=True
    )

    cards = []
    for obj in objects:
        types = ", ".join(f"{ext} × {count}" for ext, count in obj.get("top_file_types", [])[:3])
        modified = obj.get("last_modified") or "暂无"
        git = "Git 仓库" if obj.get("git_repo") else "普通目录"
        cards.append(f"""
        <section class="card">
          <h3>{html.escape(obj.get("name","未命名"))}</h3>
          <div class="meta">
            文件：{obj.get("file_count",0)}<br>
            最近更新：{html.escape(modified)}<br>
            类型：{html.escape(types or "暂无")}
          </div>
          <span class="badge">{git}</span>
        </section>
        """)

    output = workspace / ".lujiaojue" / "workbench.html"
    output.write_text(
        HTML.format(cards="\n".join(cards), generated_at=html.escape(data.get("generated_at",""))),
        encoding="utf-8"
    )
    print(f"Written: {output}")

if __name__ == "__main__":
    main()
