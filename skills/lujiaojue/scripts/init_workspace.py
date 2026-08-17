#!/usr/bin/env python3
"""鹿角蕨 v0.3：只读扫描工作文件夹，发现减熵、提效、成果与复利线索。"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

IGNORE_DIRS = {
    ".git", ".lujiaojue", ".venv", "venv", "node_modules",
    "__pycache__", ".idea", ".vscode", "Library", ".cache"
}

KEYWORDS = (
    "readme", "方案", "计划", "进度", "决策", "纪要", "成果", "汇报",
    "验收", "交付", "手册", "指南", "课程", "案例", "模板", "方法",
    "project", "plan", "roadmap", "report", "deliverable", "manual",
    "guide", "template", "case"
)

RESULT_KEYWORDS = (
    "成果", "验收", "交付", "汇报", "总结", "发布", "结项",
    "deliverable", "result", "report", "release", "final"
)

ASSET_KEYWORDS = (
    "资源", "资源池", "讲师池", "模板", "案例", "方法", "手册", "指南",
    "课程", "课件", "研究", "素材", "标准", "知识", "作品",
    "workflow", "skill", "template", "case", "manual", "guide", "research"
)

TEMP_HINTS = (
    "副本", "copy", "临时", "temp", "tmp", "未命名", "untitled"
)

VERSION_HINT_RE = re.compile(
    r"(最终版?|最新版?|终版|final|latest|v\d+(?:\.\d+){0,2}|"
    r"修订版?|修改版?|new|新版|副本|copy(?:\s*\d+)?)",
    re.I,
)

SAFE_MAX_TOP_ENTRIES = 250
STALE_DAYS = 120


def utc_now():
    return datetime.now(timezone.utc)


def iso_mtime(path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
    except OSError:
        return None


def days_since(ts: float) -> int:
    return max(0, int((utc_now().timestamp() - ts) // 86400))


def normalize_version_name(path: Path) -> str:
    """Conservative normalization for obvious version/copy variants."""
    stem = path.stem.lower()
    stem = VERSION_HINT_RE.sub("", stem)
    stem = re.sub(r"[\s_\-（）()【】\[\].]+", "", stem)
    stem = re.sub(r"\d{6,8}$", "", stem)  # trailing compact dates
    return stem + path.suffix.lower()


def is_forbidden_broad_root(path: Path) -> bool:
    resolved = path.resolve()
    # filesystem root
    if resolved == Path(resolved.anchor):
        return True
    # user home
    try:
        if resolved == Path.home().resolve():
            return True
    except Exception:
        pass
    return False


def walk_files(base: Path, depth: int = 3):
    for p in base.rglob("*"):
        try:
            rel = p.relative_to(base)
        except ValueError:
            continue
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if len(rel.parts) > depth:
            continue
        if p.is_file():
            yield p, rel


def summarize_dir(path: Path):
    file_count = 0
    ext_counter = Counter()
    newest_ts = 0.0
    key_files = []
    result_files = []

    for p, rel in walk_files(path, depth=3):
        file_count += 1
        ext_counter[p.suffix.lower() or "[no-ext]"] += 1
        try:
            newest_ts = max(newest_ts, p.stat().st_mtime)
        except OSError:
            pass

        lname = p.name.lower()
        if any(k in lname for k in KEYWORDS):
            key_files.append(str(rel))
        if any(k in lname for k in RESULT_KEYWORDS):
            result_files.append(str(rel))

    newest = (
        datetime.fromtimestamp(newest_ts, tz=timezone.utc).isoformat()
        if newest_ts else None
    )
    return {
        "name": path.name,
        "path": str(path),
        "file_count": file_count,
        "top_file_types": ext_counter.most_common(5),
        "last_modified": newest,
        "days_since_update": days_since(newest_ts) if newest_ts else None,
        "git_repo": (path / ".git").exists(),
        "key_files": key_files[:12],
        "result_files": result_files[:8],
    }


def entropy_signals(workspace: Path):
    groups = defaultdict(list)
    temp_candidates = []
    all_files = []

    for p, rel in walk_files(workspace, depth=4):
        all_files.append((p, rel))
        norm = normalize_version_name(p)
        if norm and len(norm) >= 4:
            groups[norm].append(str(rel))
        lname = p.name.lower()
        if any(h in lname for h in TEMP_HINTS):
            temp_candidates.append(str(rel))

    version_groups = []
    for norm, items in groups.items():
        # Only surface groups where at least one name has a version/copy marker.
        if len(items) < 2:
            continue
        if any(VERSION_HINT_RE.search(Path(x).stem) for x in items):
            version_groups.append({
                "normalized": norm,
                "files": sorted(items)[:8],
                "count": len(items),
                "label": "可能存在多个版本"
            })

    version_groups.sort(key=lambda x: (-x["count"], x["normalized"]))

    return {
        "version_groups": version_groups[:12],
        "temporary_candidates": sorted(temp_candidates)[:20],
    }


def repeated_structure_signals(workspace: Path):
    """Find key filenames/patterns repeated across multiple top-level work dirs."""
    occurrences = defaultdict(set)
    samples = defaultdict(list)

    top_dirs = [p for p in workspace.iterdir()
                if p.is_dir() and not p.name.startswith(".") and p.name not in IGNORE_DIRS]

    for d in top_dirs:
        for p, rel in walk_files(d, depth=3):
            lname = p.name.lower()
            if any(k in lname for k in KEYWORDS):
                key = normalize_version_name(p)
                if key:
                    occurrences[key].add(d.name)
                    samples[key].append(f"{d.name}/{rel}")

    repeated = []
    for key, dirs in occurrences.items():
        if len(dirs) >= 3:
            repeated.append({
                "pattern": key,
                "work_count": len(dirs),
                "works": sorted(dirs)[:8],
                "samples": samples[key][:6],
                "label": "重复结构候选"
            })

    repeated.sort(key=lambda x: (-x["work_count"], x["pattern"]))
    return repeated[:10]


def asset_candidates(workspace: Path, objects):
    candidates = []
    seen = set()

    # Directory-name signals
    for obj in objects:
        lname = obj["name"].lower()
        if any(k in lname for k in ASSET_KEYWORDS):
            key = obj["path"]
            if key not in seen:
                candidates.append({
                    "name": obj["name"],
                    "path": obj["path"],
                    "reason": "目录名称显示它可能是长期维护的资源或成果",
                    "kind": "长期资产候选"
                })
                seen.add(key)

    # Key/result files suggesting reusable artifacts.
    for obj in objects:
        for rel in obj.get("key_files", []):
            lname = rel.lower()
            if any(k in lname for k in ASSET_KEYWORDS):
                key = obj["path"] + "::" + rel
                if key not in seen:
                    candidates.append({
                        "name": f'{obj["name"]} / {rel}',
                        "path": key,
                        "reason": "文件名称显示它可能具有跨任务复用价值",
                        "kind": "长期资产候选"
                    })
                    seen.add(key)

    return candidates[:12]


def change_summary(previous, current_objects):
    if not previous:
        return {"has_previous": False, "changed": [], "new": [], "quiet": []}

    prev_by_path = {
        x.get("path"): x for x in previous.get("candidate_work_objects", [])
        if x.get("path")
    }
    cur_by_path = {x.get("path"): x for x in current_objects if x.get("path")}

    changed, new, quiet = [], [], []
    for path, cur in cur_by_path.items():
        prev = prev_by_path.get(path)
        if not prev:
            new.append(cur["name"])
            continue
        if (cur.get("last_modified") != prev.get("last_modified")
                or cur.get("file_count") != prev.get("file_count")):
            changed.append(cur["name"])
        elif cur.get("days_since_update") is not None and cur["days_since_update"] >= STALE_DAYS:
            quiet.append(cur["name"])

    return {
        "has_previous": True,
        "changed": changed[:12],
        "new": new[:12],
        "quiet": quiet[:12],
    }


def main():
    parser = argparse.ArgumentParser(description="初始化或刷新鹿角蕨工作文件夹。")
    parser.add_argument("folder", help="用户当前工作的文件夹")
    parser.add_argument("--dry-run", action="store_true", help="只输出，不写入 .lujiaojue")
    parser.add_argument("--allow-broad", action="store_true", help="允许扫描较宽范围（高级用户）")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        raise SystemExit(f"不是文件夹：{folder}")

    if not args.allow_broad and is_forbidden_broad_root(folder):
        raise SystemExit(
            "这个范围太大。请先打开一个你平时真正工作的文件夹，"
            "例如“工作”“项目”或某个具体业务目录，而不是整个磁盘或用户主目录。"
        )

    top_entries = [
        p for p in folder.iterdir()
        if not p.name.startswith(".") and p.name not in IGNORE_DIRS
    ]
    if not args.allow_broad and len(top_entries) > SAFE_MAX_TOP_ENTRIES:
        raise SystemExit(
            f"这个文件夹顶层已有 {len(top_entries)} 个项目，范围可能过大。"
            "建议先选择一个更具体的工作文件夹。"
        )

    state_dir = folder / ".lujiaojue"
    state_file = state_dir / "workspace.json"
    previous = None
    if state_file.exists():
        try:
            previous = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            previous = None

    objects = []
    for child in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if child.name.startswith(".") or child.name in IGNORE_DIRS:
            continue
        if child.is_dir():
            objects.append(summarize_dir(child))

    root_files = []
    for p in folder.iterdir():
        if p.is_file() and not p.name.startswith("."):
            root_files.append({
                "name": p.name,
                "path": str(p),
                "last_modified": iso_mtime(p),
                "size": p.stat().st_size,
            })

    ent = entropy_signals(folder)
    repeated = repeated_structure_signals(folder)
    assets = asset_candidates(folder, objects)
    changes = change_summary(previous, objects)

    active = sorted(
        [o for o in objects if o.get("last_modified")],
        key=lambda x: x["last_modified"],
        reverse=True
    )[:8]

    stale = [
        {"name": o["name"], "days_since_update": o["days_since_update"]}
        for o in objects
        if o.get("days_since_update") is not None and o["days_since_update"] >= STALE_DAYS
    ][:10]

    outcome_candidates = []
    for o in active:
        if o.get("result_files"):
            outcome_candidates.append({
                "name": o["name"],
                "result_files": o["result_files"],
                "label": "成果线索"
            })

    data = {
        "schema_version": 2,
        "generated_at": utc_now().isoformat(),
        "folder_root": str(folder),
        "internal_workspace_root": str(folder),
        "principle": "entropy-first-map-first-no-move",
        "candidate_work_objects": objects,
        "root_files": sorted(
            root_files,
            key=lambda x: x.get("last_modified") or "",
            reverse=True
        )[:30],
        "signals": {
            "entropy": {
                **ent,
                "stale_candidates": stale,
            },
            "efficiency": {
                "repeated_structures": repeated,
            },
            "outcomes": {
                "active_works": [
                    {
                        "name": o["name"],
                        "path": o["path"],
                        "last_modified": o["last_modified"],
                        "file_count": o["file_count"],
                        "git_repo": o["git_repo"],
                        "key_files": o["key_files"][:5],
                    }
                    for o in active
                ],
                "result_candidates": outcome_candidates[:8],
            },
            "compounding": {
                "asset_candidates": assets,
            },
            "changes": changes,
        },
    }

    print(json.dumps(data, ensure_ascii=False, indent=2))

    if not args.dry_run:
        state_dir.mkdir(exist_ok=True)
        state_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        print(f"\n已写入：{state_file}")


if __name__ == "__main__":
    main()
