from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FIXED_DESCRIPTION = (
    "Analyze UI screen recording videos and convert them into structured UI understanding "
    "reports, including screens, components, actions, states, transitions, and implementation notes."
)

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
    frontmatter_lines = lines[1:end_index]
    body = "\n".join(lines[end_index + 1 :])

    data = {}
    current_key = None
    current_list = []
    for line in frontmatter_lines:
        if line.startswith("  - "):
            current_list.append(line[4:].strip())
            continue
        if current_key is not None and current_list:
            data[current_key] = current_list
            current_key = None
            current_list = []
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = value
        else:
            current_key = key
            current_list = []
    if current_key is not None:
        data[current_key] = current_list
    return data, body


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


def test_skill_frontmatter_is_fixed() -> None:
    frontmatter, body = parse_frontmatter(read_text("SKILL.md"))
    assert frontmatter == {
        "name": "video-ui-understanding",
        "description": FIXED_DESCRIPTION,
        "version": "0.1.0",
        "license": "MIT",
        "tags": [
            "video",
            "ui",
            "ux",
            "screen-recording",
            "product-spec",
            "frontend",
            "coding-agent",
            "implementation-agent",
            "codex",
        ],
    }
    assert "video-ui-to-codex" in body
    assert "Do not rename this skill" in body


def test_skill_json_metadata() -> None:
    data = json.loads(read_text("skill.json"))
    assert data["name"] == "video-ui-understanding"
    assert data["entry"] == "SKILL.md"
    assert data["license"] == "MIT"
    assert data["tags"] == [
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


def test_readme_contains_required_install_commands_and_sections() -> None:
    text = read_text("README.md")
    for section in [
        "## Project Summary",
        "## Suitable Use Cases",
        "## Not Suitable For",
        "## Installation",
        "## Recommended Dependency Installation",
        "## Script Usage",
        "## Output Format",
        "## Safety Boundaries",
        "## Limitations",
        "## License",
    ]:
        assert section in text
    assert "openclaw skills install https://github.com/mistyShen/openclaw-video-ui-understanding" in text
    assert "git clone https://github.com/mistyShen/openclaw-video-ui-understanding.git" in text
    assert "openclaw skills install ./openclaw-video-ui-understanding --as video-ui-understanding" in text
    owner_placeholder = "<" + "owner>"
    local_users_path = "/" + "Users/"
    assert owner_placeholder not in text
    assert local_users_path not in text
    assert "mistyShen/openclaw-video-ui-understanding" in text
    assert "(templates/ui-understanding-output.md)" in text
    assert "(templates/implementation-agent-prompt-output.md)" in text
    assert "(LICENSE)" in text
    assert "implementation-agent prompt" in text
    assert "The generated implementation prompt is tool-agnostic" in text
    assert "Claude Code, Cursor, Windsurf, Aider, OpenHands, OpenClaw agents, Codex" in text


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


def test_implementation_agent_prompt_template_contains_fixed_implementation_rules() -> None:
    assert not (PROJECT_ROOT / "templates" / "codex-prompt-output.md").exists()
    text = read_text("templates/implementation-agent-prompt-output.md")
    for phrase in [
        "Inspect the existing project structure before making changes.",
        "Reuse existing components, routes, state management, and styling systems.",
        "Implement only functionality clearly visible",
        "unable to confirm",
        "Run the project existing lint, test, and build commands.",
        "Output the modified file list.",
        "Output verification results.",
        "Do not call any specific coding-agent SDK or API.",
    ]:
        assert phrase in text
