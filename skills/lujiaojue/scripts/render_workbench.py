#!/usr/bin/env python3
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path

def esc(v):
    return html.escape(str(v))

def block(label, value, sub=""):
    if not value:
        return ""
    sub_html = '<div class="sub">' + esc(sub) + '</div>' if sub else ""
    return (
        '<section class="value-block">'
        '<div class="label">' + esc(label) + '</div>'
        '<div class="value">' + esc(value) + '</div>'
        + sub_html +
        '</section>'
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    state_file = folder / ".lujiaojue" / "workspace.json"
    if not state_file.exists():
        raise SystemExit("还没有小鹿工作状态。请先运行小鹿启动。")

    data = json.loads(state_file.read_text(encoding="utf-8"))
    sig = data.get("signals", {})
    outcomes = sig.get("outcomes", {})
    entropy = sig.get("entropy", {})
    efficiency = sig.get("efficiency", {})
    compounding = sig.get("compounding", {})

    ws = data.get("work_state", {})

    # These five blocks require Agent/human judgment.
    # Do not infer them from file names or activity alone.
    final_outcome = ws.get("final_outcome")
    key_time = ws.get("key_time")
    current_focus = ws.get("current_focus")
    pending_decision = ws.get("pending_decision")
    risk = ws.get("risk")

    primary = "".join([
        block("最终成果", final_outcome),
        block("关键时间", key_time),
        block("现在先做", current_focus),
        block("待决策", pending_decision),
        block("风险", risk),
    ]) or '<div class="empty">还没有足够信息形成当前工作判断。</div>'

    version_groups = entropy.get("version_groups", [])
    repeated = efficiency.get("repeated_structures", [])
    assets = compounding.get("asset_candidates", [])

    cleanup = str(len(version_groups)) + " 组版本需要确认" if version_groups else None
    saving = (
        str(repeated[0].get("work_count", 0)) + " 项工作出现稳定重复结构"
        if repeated else None
    )
    lasting = str(len(assets)) + " 个长期成果候选" if assets else None

    secondary = "".join([
        block("需要收敛", cleanup),
        block("可以省下来", saving),
        block("最近留下来的", lasting),
    ])

    template = (Path(__file__).resolve().parent.parent / "ui" / "workbench.html").read_text(encoding="utf-8")
    rendered = (
        template
        .replace("{{FOLDER_NAME}}", esc(folder.name))
        .replace("{{PRIMARY}}", primary)
        .replace("{{SECONDARY}}", secondary)
        .replace("{{GENERATED_AT}}", esc(data.get("generated_at", "")))
    )

    out = folder / ".lujiaojue" / "workbench.html"
    out.write_text(rendered, encoding="utf-8")
    print("已生成：" + str(out))

if __name__ == "__main__":
    main()
