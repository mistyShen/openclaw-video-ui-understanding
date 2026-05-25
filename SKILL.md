---
name: video-ui-understanding
description: Analyze UI screen recording videos and convert them into structured UI understanding reports, including screens, components, actions, states, transitions, and implementation notes.
version: 0.1.0
license: MIT
tags:
  - video
  - ui
  - ux
  - screen-recording
  - product-spec
  - frontend
  - coding-agent
  - implementation-agent
  - codex
---

# Video UI Understanding

Use this skill for local UI screen recording videos or product demo videos when the user needs a structured UI understanding report and, optionally, an Implementation Agent Prompt.

## Fixed Skill Contract

- The repository root must directly contain `SKILL.md`.
- The skill name is fixed as `video-ui-understanding`.
- Do not place `SKILL.md` in a subdirectory.
- Do not rename this skill to `video-ui-to-codex`, `ui-video-parser`, `screenflow`, or any other name.

## Output Format Contract

The UI understanding report must contain these sections exactly:

- A. Source Summary
- B. Product / Function Goal
- C. Screen Inventory
- D. Timeline of Interactions
- E. UI Element Inventory
- F. State and Interaction Rules
- G. Form and Data Requirements
- H. Inferred Data / API Needs
- I. Visual and Layout Notes
- J. Unclear or Unconfirmed Details
- K. Implementation Notes
- L. Optional Implementation Agent Prompt

The timeline table must use this header:

```md
| Step | Time / Frame | Screen | User Action | System Response | Evidence | Confidence | Notes |
|---|---|---|---|---|---|---|---|
```

`Confidence` must be only `high`, `medium`, or `low`.

`Evidence` must cite a timestamp, frame number, or screenshot basis.

Any UI detail that is not visible, is too blurry, is too fast, or cannot be verified must be placed in `J. Unclear or Unconfirmed Details`. Use `unable to confirm` or `unclear`; do not guess.

Do not state speculation as fact. Do not invent pages, buttons, fields, routes, APIs, states, or behaviors that do not appear in the video. Every inference must include `Evidence` and `Confidence`.

## Script CLI Contract

The bundled scripts expose these fixed interfaces:

```bash
python3 scripts/inspect_video.py <video_path>
python3 scripts/extract_video_frames.py <video_path> --fps 1 --out <frames_dir>
python3 scripts/make_contact_sheet.py <frames_dir> --out <contact_sheet_path> --cols 4 --thumb-width 320
```

- `inspect_video.py` uses `ffprobe`. If `ffprobe` is unavailable, it must print a clear error and return a non-zero exit code.
- `extract_video_frames.py` defaults to `--fps 1`.
- Fast UI videos may benefit from `--fps 2`, but the script must not change that automatically.
- Extracted frames default to JPG.
- Frame names are fixed as `frame_0001.jpg`, `frame_0002.jpg`, `frame_0003.jpg`, and so on.
- Existing frame outputs are not overwritten unless `--overwrite` is explicitly passed.
- `make_contact_sheet.py` defaults to `--cols 4` and `--thumb-width 320`.
- All scripts must support `--help`.
- Script failures must return non-zero exit codes with clear error messages.
- Scripts must not delete or overwrite the input video.
- Scripts must not write to unknown locations; outputs require explicit `--out` where files are written.

## Dependency Contract

Version 0.1.0 only allows:

- Python >= 3.9
- Optional local system dependency: `ffmpeg`
- Optional local system dependency: `ffprobe`
- Optional Python dependency: Pillow, only for contact sheet generation
- Test dependency: pytest

Do not add OpenCV, moviepy, selenium, playwright, cloud API SDKs, databases, web servers, upload services, telemetry, background services, or browser automation dependencies.

## Safety Contract

- Do not upload videos, frames, screenshots, metadata, or reports to third parties.
- Do not delete the original video.
- Do not overwrite the original video.
- Do not read unrelated user directories.
- Do not read browser passwords, cookies, SSH keys, API keys, or other credentials.
- Do not install dependencies unless the user explicitly agrees.
- Do not automatically modify a codebase.
- Do not automatically publish, send, or exfiltrate analysis results.
- If passwords, tokens, private messages, personal data, or sensitive information appears in the video, redact it in the report.
- Mark uncertain information as `unable to confirm` or `unclear`; do not guess.
- Do not add telemetry, log upload, or remote callback behavior.
- Do not automatically call paid APIs.
- Do not process private videos over the network by default.

## Project Boundary

This version only supports:

- UI video understanding reports
- Optional implementation-agent prompt generation
- Optional local frame extraction
- Optional local contact sheet generation

Do not add automatic code implementation, automatic coding-agent launch, automatic Git commits, automatic publishing, network analysis for private video, paid API calls, cookie access, browser opening, screen recording, folder monitoring, background services, or a Web UI.

## Recommended Workflow

1. Inspect the video locally with `scripts/inspect_video.py`.
2. Extract frames locally with `scripts/extract_video_frames.py` when `ffmpeg` is available.
3. Create a local contact sheet with `scripts/make_contact_sheet.py` when Pillow is available.
4. Fill `templates/ui-understanding-output.md` from evidence only.
5. Optionally fill `templates/implementation-agent-prompt-output.md` for implementation guidance.
