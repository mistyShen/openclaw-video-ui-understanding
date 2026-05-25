#!/usr/bin/env python3
"""Extract frames from a local video with ffmpeg."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract JPG frames from a local video file into an explicit output directory."
    )
    parser.add_argument("video", help="Path to a local video file")
    parser.add_argument(
        "--fps",
        type=float,
        default=1.0,
        help="Frames per second to extract (default: 1.0)",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Directory to write extracted frames into",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting existing frame_*.jpg files in the output directory",
    )
    return parser


def extract_frames(video_path: Path, output_dir: Path, fps: float, overwrite: bool) -> int:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError(
            "ffmpeg is not available on PATH. Install it manually if you need frame extraction."
        )
    if fps <= 0:
        raise ValueError("fps must be greater than 0")
    if not video_path.is_file():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    existing_frames = sorted(output_dir.glob("frame_*.jpg"))
    if existing_frames and not overwrite:
        raise RuntimeError(
            "Output directory already contains frame_*.jpg files. Pass --overwrite to replace them."
        )

    output_pattern = output_dir / "frame_%04d.jpg"
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if overwrite else "-n",
        "-i",
        str(video_path),
        "-vf",
        f"fps={fps}",
        "-q:v",
        "2",
        str(output_pattern),
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "unknown ffmpeg error"
        raise RuntimeError(f"ffmpeg failed: {stderr}")

    return len(list(output_dir.glob("frame_*.jpg")))


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        frame_count = extract_frames(
            Path(args.video),
            Path(args.out),
            args.fps,
            args.overwrite,
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"extracted_frames={frame_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
