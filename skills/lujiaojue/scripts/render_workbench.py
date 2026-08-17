#!/usr/bin/env python3
from __future__ import annotations
import argparse, html, json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--template", default=None)
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    state_file = workspace / ".lujiaojue" / "workspace.json"
    if not state_file.exists():
        raise SystemExit("未找到 .lujiaojue/workspace.json，请先执行鹿角蕨初始化。")

    data = json.loads(state_file.read_text(encoding="utf-8"))
    if args.template:
        template_path = Path(args.template)
    else:
        template_path = Path(__file__).resolve().parent.parent / "ui" / "workbench.html"

    template = template_path.read_text(encoding="utf-8")
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
        cards.append(
            '<section class="card">'
            f'<h3>{html.escape(obj.get("name","未命名"))}</h3>'
            '<div class="meta">'
            f'文件：{obj.get("file_count",0)}<br>'
            f'最近更新：{html.escape(modified)}<br>'
            f'类型：{html.escape(types or "暂无")}'
            '</div>'
            f'<span class="badge">{git}</span>'
            '</section>'
        )

    output = workspace / ".lujiaojue" / "workbench.html"
    output.write_text(
        template.replace("{{CARDS}}", "\n".join(cards))
                .replace("{{GENERATED_AT}}", html.escape(data.get("generated_at",""))),
        encoding="utf-8"
    )
    print(f"Written: {output}")

if __name__ == "__main__":
    main()
