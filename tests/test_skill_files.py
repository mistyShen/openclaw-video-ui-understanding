from __future__ import annotations

import subprocess
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_TAGS = {
    "video",
    "ui",
    "ux",
    "screen-recording",
    "product-spec",
    "frontend",
    "coding-agent",
    "implementation-agent",
    "codex",
}


def read_text(path: str) -> str:
    return (PROJECT_ROOT / path).read_text(encoding="utf-8")


def parse_skill_frontmatter() -> dict:
    lines = read_text("SKILL.md").splitlines()
    assert lines[0] == "---"
    end = lines.index("---", 1)
    assert lines[end] == "---"
    assert lines[end + 1] == ""
    return yaml.safe_load("\n".join(lines[1:end]))


def grep_repo(pattern: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["grep", "-R", pattern, ".", "--exclude-dir=.git"],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_readme_install_metadata_is_public_ready() -> None:
    text = read_text("README.md")
    assert "<" + "owner>" not in text
    assert "github.com" + "//" not in text
    assert "/" + "Users/" not in text
    assert "https://github.com/mistyShen/openclaw-video-ui-understanding" in text
    assert "openclaw skills install https://github.com/mistyShen/openclaw-video-ui-understanding" in text
    assert "git clone https://github.com/mistyShen/openclaw-video-ui-understanding.git" in text
    assert "openclaw skills install ./openclaw-video-ui-understanding --as video-ui-understanding" in text


def test_skill_frontmatter_is_valid_yaml_and_tool_agnostic() -> None:
    data = parse_skill_frontmatter()
    assert data["name"] == "video-ui-understanding"
    assert data["version"] == "0.1.0"
    assert REQUIRED_TAGS.issubset(set(data["tags"]))


def test_required_files_exist_and_old_codex_template_is_absent() -> None:
    required_paths = [
        "README.md",
        "SECURITY.md",
        "LICENSE",
        "SKILL.md",
        "scripts/inspect_video.py",
        "scripts/extract_video_frames.py",
        "scripts/make_contact_sheet.py",
        "templates/ui-understanding-output.md",
        "templates/implementation-agent-prompt-output.md",
    ]
    for path in required_paths:
        assert (PROJECT_ROOT / path).is_file(), path
    assert not (PROJECT_ROOT / "templates" / "codex-prompt-output.md").exists()


def test_security_documents_required_boundaries() -> None:
    text = read_text("SECURITY.md").lower()
    assert "no third-party upload" in text or "do not upload" in text
    assert "no telemetry" in text or "do not add telemetry" in text
    assert "no credential access" in text or "do not read browser passwords" in text


def test_repository_has_no_release_blocker_strings() -> None:
    patterns = [
        "/" + "Users/",
        "<" + "owner>",
        "github.com" + "//",
    ]
    for pattern in patterns:
        result = grep_repo(pattern)
        assert result.returncode == 1, result.stdout
        assert result.stdout == ""
