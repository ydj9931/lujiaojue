#!/usr/bin/env python3
"""把鹿角蕨扫描状态渲染成 v0.3 生长型工作台。"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def esc(v):
    return html.escape(str(v))


def card(title, body, cls=""):
    return f'<article class="item {cls}"><h3>{esc(title)}</h3>{body}</article>'


def empty(text):
    return f'<div class="empty">{esc(text)}</div>'


def entropy_html(signals):
    blocks = []
    versions = signals.get("version_groups", [])
    for g in versions[:5]:
        files = "".join(f"<li>{esc(x)}</li>" for x in g.get("files", [])[:4])
        blocks.append(card(
            f'{g.get("count", 0)} 个可能版本',
            f'<p class="muted">建议先确认哪一份代表当前事实。</p><ul>{files}</ul>',
            "attention"
        ))

    temps = signals.get("temporary_candidates", [])
    if temps:
        blocks.append(card(
            "明显副本 / 临时文件候选",
            f'<p class="big-number">{len(temps)}</p>'
            '<p class="muted">只提示，不自动删除。</p>',
            "soft"
        ))

    stale = signals.get("stale_candidates", [])
    if stale:
        sample = "、".join(x["name"] for x in stale[:4])
        blocks.append(card(
            "长期未更新候选",
            f'<p>{esc(sample)}</p><p class="muted">它们不一定无用，只值得确认是否仍属于当前工作。</p>',
            "soft"
        ))

    return "".join(blocks) or empty("暂未发现明显的文件熵增信号。")


def efficiency_html(signals):
    repeated = signals.get("repeated_structures", [])
    blocks = []
    for r in repeated[:5]:
        works = " · ".join(r.get("works", [])[:5])
        blocks.append(card(
            "重复结构候选",
            f'<p class="big-number">{r.get("work_count", 0)} 项工作</p>'
            f'<p>{esc(works)}</p>'
            '<p class="muted">先验证是否真的重复，再决定做模板、Workflow 或 Skill。</p>',
            "growth"
        ))
    return "".join(blocks) or empty("还没有足够证据说明某类工作已经稳定重复。继续工作即可。")


def outcomes_html(signals):
    active = signals.get("active_works", [])
    blocks = []
    for w in active[:6]:
        key_files = w.get("key_files", [])
        keys = ""
        if key_files:
            keys = '<div class="chips">' + "".join(
                f'<span>{esc(x)}</span>' for x in key_files[:3]
            ) + "</div>"
        git = '<span class="mini">Git</span>' if w.get("git_repo") else ""
        blocks.append(card(
            w.get("name", "未命名工作"),
            f'<div class="row"><span>{w.get("file_count",0)} 个文件</span>{git}</div>'
            f'{keys}',
            "active"
        ))
    return "".join(blocks) or empty("暂未识别到近期活跃的主要工作。")


def compounding_html(signals):
    assets = signals.get("asset_candidates", [])
    blocks = []
    for a in assets[:6]:
        blocks.append(card(
            a.get("name", "长期资产候选"),
            f'<p class="muted">{esc(a.get("reason",""))}</p>'
            '<span class="candidate">候选</span>',
            "compound"
        ))
    return "".join(blocks) or empty("暂未发现明确的长期资产候选。不要为了复利强行制造项目。")


def changes_html(signals):
    if not signals.get("has_previous"):
        return '<span>这是第一次扫描，我还没有上一版可以比较。</span>'
    parts = []
    if signals.get("changed"):
        parts.append("更新：" + "、".join(signals["changed"][:5]))
    if signals.get("new"):
        parts.append("新增：" + "、".join(signals["new"][:5]))
    if not parts:
        parts.append("与上次扫描相比，没有发现明显结构变化。")
    return esc("；".join(parts))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="用户当前工作的文件夹")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    state_file = folder / ".lujiaojue" / "workspace.json"
    if not state_file.exists():
        raise SystemExit("还没有初始化。请先运行“鹿角蕨初始化”。")

    data = json.loads(state_file.read_text(encoding="utf-8"))
    template_path = Path(__file__).resolve().parent.parent / "ui" / "workbench.html"
    template = template_path.read_text(encoding="utf-8")

    signals = data.get("signals", {})
    rendered = (
        template
        .replace("{{FOLDER_NAME}}", esc(folder.name))
        .replace("{{GENERATED_AT}}", esc(data.get("generated_at", "")))
        .replace("{{CHANGES}}", changes_html(signals.get("changes", {})))
        .replace("{{ENTROPY}}", entropy_html(signals.get("entropy", {})))
        .replace("{{EFFICIENCY}}", efficiency_html(signals.get("efficiency", {})))
        .replace("{{OUTCOMES}}", outcomes_html(signals.get("outcomes", {})))
        .replace("{{COMPOUNDING}}", compounding_html(signals.get("compounding", {})))
    )

    output = folder / ".lujiaojue" / "workbench.html"
    output.write_text(rendered, encoding="utf-8")
    print(f"已生成：{output}")


if __name__ == "__main__":
    main()
