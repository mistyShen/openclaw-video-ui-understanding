#!/usr/bin/env python3
"""Create a contact sheet from a directory of extracted frames."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a contact sheet image from extracted frame images."
    )
    parser.add_argument("frames_dir", help="Directory containing frame images")
    parser.add_argument(
        "--out",
        required=True,
        help="Path to the output contact sheet image",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=4,
        help="Number of columns in the contact sheet (default: 4)",
    )
    parser.add_argument(
        "--thumb-width",
        type=int,
        default=320,
        help="Thumbnail width in pixels (default: 320)",
    )
    parser.add_argument(
        "--background",
        default="white",
        help="Background color passed to Pillow (default: white)",
    )
    return parser


def make_contact_sheet(
    frames_dir: Path,
    output_image: Path,
    columns: int,
    thumb_width: int,
    background: str,
) -> int:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is required for contact sheet generation. Install it manually with 'python3 -m pip install pillow'."
        ) from exc

    if columns <= 0:
        raise ValueError("columns must be greater than 0")
    if thumb_width <= 0:
        raise ValueError("thumb-width must be greater than 0")
    if not frames_dir.is_dir():
        raise FileNotFoundError(f"Frames directory not found: {frames_dir}")

    image_paths = sorted(
        path
        for path in frames_dir.iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    if not image_paths:
        raise RuntimeError("No supported frame images were found in the frames directory.")

    thumbnails = []
    for image_path in image_paths:
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            height = max(1, int(image.height * (thumb_width / image.width)))
            thumbnail = image.resize((thumb_width, height))
            thumbnails.append(thumbnail)

    max_height = max(image.height for image in thumbnails)
    rows = math.ceil(len(thumbnails) / columns)
    sheet = Image.new(
        "RGB",
        (columns * thumb_width, rows * max_height),
        color=background,
    )

    for index, image in enumerate(thumbnails):
        x = (index % columns) * thumb_width
        y = (index // columns) * max_height
        sheet.paste(image, (x, y))

    output_image.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_image)
    return len(thumbnails)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        image_count = make_contact_sheet(
            Path(args.frames_dir),
            Path(args.out),
            args.cols,
            args.thumb_width,
            args.background,
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"images_in_sheet={image_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
