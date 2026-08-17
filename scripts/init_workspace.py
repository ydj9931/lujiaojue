#!/usr/bin/env python3
"""鹿角蕨 v0.1 工作空间初始化：只扫描，不搬文件。"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

IGNORE_DIRS = {
    ".git", ".lujiaojue", ".venv", "venv", "node_modules",
    "__pycache__", ".idea", ".vscode"
}
KEYWORDS = (
    "readme", "方案", "计划", "进度", "决策", "纪要",
    "成果", "汇报", "验收", "project", "plan", "roadmap"
)

def iso_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()

def summarize_dir(path: Path, max_depth: int = 2):
    file_count = 0
    ext_counter = Counter()
    newest_ts = 0.0
    key_files = []
    git_repo = (path / ".git").exists()

    for p in path.rglob("*"):
        try:
            rel = p.relative_to(path)
        except ValueError:
            continue
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if len(rel.parts) > max_depth + 1:
            continue
        if p.is_file():
            file_count += 1
            ext_counter[p.suffix.lower() or "[no-ext]"] += 1
            try:
                newest_ts = max(newest_ts, p.stat().st_mtime)
            except OSError:
                pass
            lower_name = p.name.lower()
            if any(k in lower_name for k in KEYWORDS):
                key_files.append(str(rel))

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
        "git_repo": git_repo,
        "key_files": key_files[:12],
    }

def main():
    parser = argparse.ArgumentParser(description="Initialize a Lujiaojue workspace.")
    parser.add_argument("workspace", help="目标工作目录")
    parser.add_argument("--dry-run", action="store_true", help="只输出，不写入 .lujiaojue")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.is_dir():
        raise SystemExit(f"Not a directory: {workspace}")

    objects = []
    for child in sorted(workspace.iterdir(), key=lambda p: p.name.lower()):
        if child.name in IGNORE_DIRS or child.name.startswith("."):
            continue
        if child.is_dir():
            objects.append(summarize_dir(child))

    root_files = []
    for p in workspace.iterdir():
        if p.is_file() and not p.name.startswith("."):
            root_files.append({
                "name": p.name,
                "last_modified": iso_mtime(p),
                "size": p.stat().st_size,
            })

    data = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace_root": str(workspace),
        "principle": "map-first-no-move",
        "candidate_work_objects": objects,
        "root_files": sorted(root_files, key=lambda x: x["last_modified"], reverse=True)[:30],
    }

    print(json.dumps(data, ensure_ascii=False, indent=2))

    if not args.dry_run:
        state_dir = workspace / ".lujiaojue"
        state_dir.mkdir(exist_ok=True)
        out = state_dir / "workspace.json"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nWritten: {out}")

if __name__ == "__main__":
    main()
