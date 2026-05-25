from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def run_help(script_name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )


def test_scripts_have_shebang() -> None:
    for script_name in [
        "inspect_video.py",
        "extract_video_frames.py",
        "make_contact_sheet.py",
    ]:
        first_line = (SCRIPTS_DIR / script_name).read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "#!/usr/bin/env python3"


def test_help_commands_succeed() -> None:
    for script_name in [
        "inspect_video.py",
        "extract_video_frames.py",
        "make_contact_sheet.py",
    ]:
        completed = run_help(script_name)
        assert completed.returncode == 0, completed.stderr
        assert "usage:" in completed.stdout.lower()


def test_extract_frames_help_exposes_fixed_cli_contract() -> None:
    completed = run_help("extract_video_frames.py")
    assert completed.returncode == 0
    assert "--fps" in completed.stdout
    assert "--out" in completed.stdout
    assert "--overwrite" in completed.stdout


def test_contact_sheet_help_exposes_fixed_cli_contract() -> None:
    completed = run_help("make_contact_sheet.py")
    assert completed.returncode == 0
    assert "--out" in completed.stdout
    assert "--cols" in completed.stdout
    assert "--thumb-width" in completed.stdout


def test_scripts_return_nonzero_on_missing_required_inputs() -> None:
    commands = [
        [
            sys.executable,
            str(SCRIPTS_DIR / "inspect_video.py"),
            str(PROJECT_ROOT / "tests" / "does-not-exist.mp4"),
        ],
        [
            sys.executable,
            str(SCRIPTS_DIR / "extract_video_frames.py"),
            str(PROJECT_ROOT / "tests" / "does-not-exist.mp4"),
            "--out",
            str(PROJECT_ROOT / "tests" / "frames-out"),
        ],
        [
            sys.executable,
            str(SCRIPTS_DIR / "make_contact_sheet.py"),
            str(PROJECT_ROOT / "tests" / "does-not-exist"),
            "--out",
            str(PROJECT_ROOT / "tests" / "contact-sheet.jpg"),
        ],
    ]
    for command in commands:
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        assert completed.returncode != 0
        assert "error:" in completed.stderr.lower()


def test_frame_extraction_source_uses_fixed_frame_pattern() -> None:
    text = (SCRIPTS_DIR / "extract_video_frames.py").read_text(encoding="utf-8")
    assert "frame_%04d.jpg" in text
    assert "frame_*.jpg" in text
