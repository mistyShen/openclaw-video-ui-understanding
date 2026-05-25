#!/usr/bin/env python3
"""Inspect a local video with ffprobe and print JSON metadata."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a local video file with ffprobe and print JSON metadata."
    )
    parser.add_argument("video", help="Path to a local video file")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    return parser


def inspect_video(video_path: Path) -> dict:
    ffprobe = shutil.which("ffprobe")
    if ffprobe is None:
        raise RuntimeError(
            "ffprobe is not available on PATH. Install it manually if you need metadata inspection."
        )
    if not video_path.is_file():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    command = [
        ffprobe,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(video_path),
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "unknown ffprobe error"
        raise RuntimeError(f"ffprobe failed: {stderr}")

    data = json.loads(completed.stdout)
    return {
        "video": str(video_path.resolve()),
        "tool": "ffprobe",
        "metadata": data,
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = inspect_video(Path(args.video))
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
