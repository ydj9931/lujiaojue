#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

FIELDS = ("final_outcome", "key_time", "current_focus", "pending_decision", "risk")

def main():
    parser = argparse.ArgumentParser(description="更新小鹿工作状态。只写入明确事实或经过判断的当前状态。")
    parser.add_argument("folder")
    parser.add_argument("--final-outcome")
    parser.add_argument("--key-time")
    parser.add_argument("--current-focus")
    parser.add_argument("--pending-decision")
    parser.add_argument("--risk")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    state_file = folder / ".lujiaojue" / "workspace.json"
    if not state_file.exists():
        raise SystemExit("尚未初始化小鹿工作状态。")

    data = json.loads(state_file.read_text(encoding="utf-8"))
    ws = data.setdefault("work_state", {})

    values = {
        "final_outcome": args.final_outcome,
        "key_time": args.key_time,
        "current_focus": args.current_focus,
        "pending_decision": args.pending_decision,
        "risk": args.risk,
    }
    for k, v in values.items():
        if v is not None:
            if v.strip():
                ws[k] = v.strip()
            else:
                ws.pop(k, None)

    state_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("工作状态已更新。")

if __name__ == "__main__":
    main()
