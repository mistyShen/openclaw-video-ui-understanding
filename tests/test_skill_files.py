from __future__ import annotations

import json
import subprocess
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FIXED_DESCRIPTION = (
    "Analyze UI screen recording videos and convert them into structured UI understanding "
    "reports, including screens, components, actions, states, transitions, and implementation notes."
)

REQUIRED_TAGS = [
    "video",
    "ui",
    "ux",
    "screen-recording",
    "product-spec",
    "frontend",
    "coding-agent",
    "implementation-agent",
    "codex",
]

REPORT_SECTIONS = [
    "## A. Source Summary",
    "## B. Product / Function Goal",
    "## C. Screen Inventory",
    "## D. Timeline of Interactions",
    "## E. UI Element Inventory",
    "## F. State and Interaction Rules",
    "## G. Form and Data Requirements",
    "## H. Inferred Data / API Needs",
    "## I. Visual and Layout Notes",
    "## J. Unclear or Unconfirmed Details",
    "## K. Implementation Notes",
    "## L. Optional Implementation Agent Prompt",
]

TIMELINE_HEADER = (
    "| Step | Time / Frame | Screen | User Action | System Response | Evidence | Confidence | Notes |\n"
    "|---|---|---|---|---|---|---|---|"
)


def read_text(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    assert lines[0] == "---"
    end_index = lines.index("---", 1)
    assert lines[end_index] == "---"
    assert lines[end_index + 1] == ""
    frontmatter = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])
    assert body.startswith("\n# ") or body.startswith("# ")
    return yaml.safe_load(frontmatter), body


def grep_repository(pattern: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["grep", "-R", pattern, ".", "--exclude-dir=.git"],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_required_files_exist() -> None:
    required_paths = [
        "SKILL.md",
        "README.md",
        "LICENSE",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "skill.json",
        "scripts/inspect_video.py",
        "scripts/extract_video_frames.py",
        "scripts/make_contact_sheet.py",
        "templates/ui-understanding-output.md",
        "templates/implementation-agent-prompt-output.md",
        "examples/README.md",
        "examples/sample-ui-flow-output.md",
        "examples/sample-implementation-agent-prompt-output.md",
        "tests/test_skill_files.py",
        "tests/test_scripts_smoke.py",
        ".github/workflows/ci.yml",
    ]
    for relative_path in required_paths:
        assert (PROJECT_ROOT / relative_path).is_file(), relative_path


def test_skill_frontmatter_is_standard_yaml() -> None:
    text = read_text("SKILL.md")
    lines = text.splitlines()
    frontmatter, body = parse_frontmatter(text)

    assert lines[0] == "---"
    assert lines.index("---", 1) > 1
    assert frontmatter["name"] == "video-ui-understanding"
    assert frontmatter["description"] == FIXED_DESCRIPTION
    assert frontmatter["version"] == "0.1.0"
    assert frontmatter["license"] == "MIT"
    assert frontmatter["tags"] == REQUIRED_TAGS
    assert "## When to Use This Skill" in body


def test_skill_json_metadata_is_tool_agnostic() -> None:
    data = json.loads(read_text("skill.json"))
    assert data["name"] == "video-ui-understanding"
    assert data["entry"] == "SKILL.md"
    assert data["license"] == "MIT"
    assert data["tags"] == REQUIRED_TAGS
    assert "implementation-agent prompts" in data["description"]


def test_readme_install_metadata_and_links() -> None:
    text = read_text("README.md")
    owner_placeholder = "<" + "owner>"
    local_users_path = "/" + "Users/"
    malformed_github = "github.com" + "//"

    assert owner_placeholder not in text
    assert local_users_path not in text
    assert malformed_github not in text
    assert "https://github.com/mistyShen/openclaw-video-ui-understanding" in text
    assert "openclaw skills install https://github.com/mistyShen/openclaw-video-ui-understanding" in text
    assert "git clone https://github.com/mistyShen/openclaw-video-ui-understanding.git" in text
    assert "openclaw skills install ./openclaw-video-ui-understanding --as video-ui-understanding" in text
    assert "(templates/ui-understanding-output.md)" in text
    assert "(templates/implementation-agent-prompt-output.md)" in text
    assert "(LICENSE)" in text
    assert "The generated implementation prompt is tool-agnostic" in text


def test_security_contains_required_boundaries() -> None:
    text = read_text("SECURITY.md").lower()
    assert "no third-party upload" in text
    assert "no telemetry" in text
    assert "no credential access" in text
    assert "browser passwords" in text
    assert "cookies" in text
    assert "ssh keys" in text
    assert "api keys" in text


def test_ui_understanding_template_contains_fixed_sections_and_timeline_header() -> None:
    text = read_text("templates/ui-understanding-output.md")
    for section in REPORT_SECTIONS:
        assert section in text
    assert TIMELINE_HEADER in text
    assert "unable to confirm" in text
    assert "high / medium / low" in text


def test_implementation_agent_prompt_template_rules_and_old_codex_template_absent() -> None:
    assert (PROJECT_ROOT / "templates" / "implementation-agent-prompt-output.md").is_file()
    assert not (PROJECT_ROOT / "templates" / "codex-prompt-output.md").exists()

    text = read_text("templates/implementation-agent-prompt-output.md")
    for phrase in [
        "Inspect the existing project structure before making changes.",
        "Reuse existing components, routes, state management, and styling systems.",
        "Implement only functionality clearly visible",
        "unable to confirm",
        "Run the project existing lint, test, and build commands when applicable.",
        "Output the modified file list.",
        "Output validation results.",
        "Do not call any specific coding-agent SDK or API.",
    ]:
        assert phrase in text


def test_repository_has_no_public_release_placeholders_or_local_paths() -> None:
    forbidden_patterns = [
        "/" + "Users/",
        "<" + "owner>",
        "github.com" + "//",
    ]
    for pattern in forbidden_patterns:
        completed = grep_repository(pattern)
        assert completed.returncode == 1, completed.stdout
        assert completed.stdout == ""
