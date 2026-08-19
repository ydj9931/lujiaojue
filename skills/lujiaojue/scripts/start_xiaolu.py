#!/usr/bin/env python3
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

def run(script: Path, folder: Path):
    subprocess.run([sys.executable, str(script), str(folder)], check=True)

def main():
    parser = argparse.ArgumentParser(description="小鹿启动：初始化、生成工作台并创建桌面入口。")
    parser.add_argument("folder", help="当前工作文件夹")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    scripts = Path(__file__).resolve().parent

    run(scripts / "init_workspace.py", folder)
    run(scripts / "render_workbench.py", folder)
    run(scripts / "create_desktop_entry.py", folder)

    print("小鹿已建立基础工作状态。")
    print("下一步应由宿主 Agent 阅读关键文件，补充最终成果、关键时间、当前重点、待决策和风险。")

if __name__ == "__main__":
    main()
