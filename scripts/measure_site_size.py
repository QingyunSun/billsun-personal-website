from __future__ import annotations

import pathlib


SITE_ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = [
    "index.html",
    "styles.css",
    "script.js",
    "assets/qingyun-sun-portrait-1280.jpg",
]


def format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    return f"{size / 1024:.1f} KB"


def main() -> None:
    total = 0
    print("Static asset footprint:")
    for name in TARGETS:
        path = SITE_ROOT / name
        size = path.stat().st_size
        total += size
        print(f"  {name:<10} {format_bytes(size)}")
    print(f"Total       {format_bytes(total)}")


if __name__ == "__main__":
    main()
