# openclaw-video-ui-understanding

`openclaw-video-ui-understanding` converts UI screen recordings into structured UI understanding reports and implementation-agent prompts.

The generated implementation prompt is tool-agnostic and can be used with coding agents such as Claude Code, Cursor, Windsurf, Aider, OpenHands, OpenClaw agents, Codex, or other compatible implementation agents.

The OpenClaw skill name remains fixed as `video-ui-understanding`.

## Project Summary

This project supports:

- UI video understanding reports
- Optional implementation-agent prompt generation
- Optional local frame extraction
- Optional local contact sheet generation

This project does not:

- Implement code automatically
- Launch coding agents automatically
- Commit Git changes automatically
- Publish content automatically
- Upload videos, frames, screenshots, metadata, or reports
- Start background services
- Provide a Web UI

## Suitable Use Cases

- Turning a product demo video into a frontend implementation brief
- Auditing a screen recording to identify visible screens, components, states, actions, and transitions
- Creating a conservative UI specification when source design files are unavailable
- Preparing an implementation-agent prompt that preserves unclear details as TODO items

## Not Suitable For

- Recovering hidden DOM structure or backend logic from video
- Automatically implementing code
- Automatically calling paid APIs
- Automatically analyzing private videos over the network
- Reading browser cookies, passwords, SSH keys, API keys, or unrelated user directories
- Monitoring folders, recording screens, opening browsers, or running background services

## Installation

### GitHub Install

```bash
openclaw skills install https://github.com/mistyShen/openclaw-video-ui-understanding
```

### Local Install

```bash
git clone https://github.com/mistyShen/openclaw-video-ui-understanding.git
openclaw skills install ./openclaw-video-ui-understanding --as video-ui-understanding
```

## Recommended Dependency Installation

Required:

```bash
python3 --version
```

Optional system dependencies:

```bash
ffprobe -version
ffmpeg -version
```

Optional Python dependency for contact sheets:

```bash
python3 -m pip install pillow
```

Test dependency:

```bash
python3 -m pip install pytest
```

This project does not install dependencies automatically. Install optional dependencies only when you explicitly choose to.

## Script Usage

Inspect local video metadata with `ffprobe`:

```bash
python3 scripts/inspect_video.py <video_path>
```

Extract JPG frames with fixed names such as `frame_0001.jpg`:

```bash
python3 scripts/extract_video_frames.py <video_path> --fps 1 --out <frames_dir>
```

For fast UI videos, consider `--fps 2`; the script does not change this automatically.

Create a contact sheet from extracted frames:

```bash
python3 scripts/make_contact_sheet.py <frames_dir> --out <contact_sheet_path> --cols 4 --thumb-width 320
```

All scripts support `--help`, return non-zero exit codes on failure, and print clear error messages.

## Output Format

Use [templates/ui-understanding-output.md](templates/ui-understanding-output.md).

The report must include:

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

The timeline table must use:

```md
| Step | Time / Frame | Screen | User Action | System Response | Evidence | Confidence | Notes |
|---|---|---|---|---|---|---|---|
```

Confidence must be one of:

- high
- medium
- low

Evidence must cite timestamps, frame numbers, or screenshot references.

Unclear details must be placed in `J. Unclear or Unconfirmed Details` and marked `unable to confirm` or `unclear`.

## Implementation Agent Prompt

Use [templates/implementation-agent-prompt-output.md](templates/implementation-agent-prompt-output.md).

The generated implementation-agent prompt must:

- Ask the agent to inspect the existing project first
- Ask the agent to reuse existing components, routes, state management, and styling systems
- Restrict implementation to visible video behavior
- Preserve unclear details as TODO items
- Require lint, test, or build validation when applicable
- Require a final changed-files and validation summary

## Safety Boundaries

- No third-party upload of videos, frames, screenshots, metadata, or reports
- No telemetry
- No credential access
- Do not read browser passwords, cookies, SSH keys, API keys, or unrelated user directories
- Do not delete the original video
- Do not overwrite the original video
- Do not automatically modify a codebase
- Do not automatically publish, send, or exfiltrate analysis results
- Do not automatically call paid APIs
- Do not process private videos over the network by default
- If passwords, tokens, private messages, personal data, or sensitive information appears in the video, redact it in the report
- If information is uncertain, mark it as `unable to confirm` or `unclear`; do not guess

## Limitations

- Video analysis is limited by resolution, compression, motion blur, cursor occlusion, and playback speed
- The skill cannot confirm hidden pages, hidden fields, APIs, data models, route structure, or backend behavior from video alone
- The skill cannot guarantee pixel-perfect visual reconstruction
- Human review is recommended before using the report as an implementation specification

## License

MIT. See [LICENSE](LICENSE).
