from __future__ import annotations

import pathlib


SITE_ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = [
    "index.html",
    "styles.css",
    "script.js",
    "assets/qingyun-sun-portrait-1280.jpg",
    "podcast/index.html",
    "podcast/podcast.css",
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
    podcast_asset_dir = SITE_ROOT / "assets" / "podcast"
    podcast_asset_total = 0
    if podcast_asset_dir.exists():
        for path in podcast_asset_dir.rglob("*"):
            if path.is_file():
                podcast_asset_total += path.stat().st_size
        total += podcast_asset_total
        print(f"  {'assets/podcast':<10} {format_bytes(podcast_asset_total)}")
    print(f"Total       {format_bytes(total)}")


if __name__ == "__main__":
    main()
