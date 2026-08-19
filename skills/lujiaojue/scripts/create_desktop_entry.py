#!/usr/bin/env python3
from __future__ import annotations
import argparse
import platform
import plistlib
from pathlib import Path

def desktop_dir():
    home = Path.home()
    for p in (home / "Desktop", home / "桌面"):
        if p.exists() and p.is_dir():
            return p
    return None

def create_entry(workbench: Path):
    desk = desktop_dir()
    if not desk:
        return None
    uri = workbench.resolve().as_uri()
    system = platform.system().lower()
    if system == "darwin":
        out = desk / "小鹿工作台.webloc"
        with out.open("wb") as f:
            plistlib.dump({"URL": uri}, f)
        return out
    if system == "windows":
        out = desk / "小鹿工作台.url"
        out.write_text("[InternetShortcut]\nURL=" + uri + "\n", encoding="utf-8")
        return out
    out = desk / "小鹿工作台.desktop"
    out.write_text(
        "[Desktop Entry]\n"
        "Type=Link\n"
        "Name=小鹿工作台\n"
        "URL=" + uri + "\n"
        "Terminal=false\n",
        encoding="utf-8",
    )
    try:
        out.chmod(0o755)
    except OSError:
        pass
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="当前工作文件夹")
    args = parser.parse_args()
    folder = Path(args.folder).expanduser().resolve()
    workbench = folder / ".lujiaojue" / "workbench.html"
    if not workbench.exists():
        raise SystemExit("尚未生成工作台。请先运行小鹿启动或刷新工作台。")
    out = create_entry(workbench)
    if out:
        print("桌面入口已更新：" + str(out))
    else:
        print("未找到桌面目录；工作台仍保存在当前工作文件夹中。")

if __name__ == "__main__":
    main()
