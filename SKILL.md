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

## When to Use This Skill

Use this skill when the user provides a UI screen recording, product demo video, app walkthrough, extracted frames, or contact sheet, and wants a structured UI understanding report.

## Inputs

The user may provide:

- A local video path
- A folder of extracted frames
- A contact sheet image
- A written description plus screenshots
- A public video link, only if the environment can legally and safely access it

## Required Safety Rules

- Do not upload the user's video to any third-party service unless the user explicitly asks for that
- Do not delete or overwrite the original video
- Do not modify the user's codebase
- Do not install packages without asking
- Do not infer private information beyond UI behavior
- Do not invent features that are not visible in the video
- If text, icons, or states are unclear, mark them as `unclear` or `unable to confirm`
- If the video contains credentials, tokens, private messages, or personal data, warn the user and avoid reproducing sensitive content

## Recommended Local Workflow

1. Locate the input video.
2. Create an output directory next to the video.
3. Inspect video metadata using `ffprobe` if available.
4. Extract frames using `ffmpeg` if needed.
5. Use 1 fps for normal UI videos.
6. Use 2 fps for fast interaction videos.
7. Generate a contact sheet if helpful.
8. Review frames in chronological order.
9. Identify page changes and interaction points.
10. Produce a structured UI understanding report.
11. If requested, produce an implementation-agent prompt.

## Analysis Method

Analyze the video as a UI and UX observer, not as a general video summarizer.

For each important time segment or frame group, identify:

- Current page or screen
- Visible UI elements
- User action
- Input text, if visible and safe
- System response
- Navigation result
- State transition
- Loading, empty, error, and success states
- Modal, drawer, popover, dropdown, toast, or alert
- List, table, or card content structure
- Form fields and validation hints
- Unclear details

## Required Output Format

Always output:

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

The timeline table must use this exact header:

```md
| Step | Time / Frame | Screen | User Action | System Response | Evidence | Confidence | Notes |
|---|---|---|---|---|---|---|---|
```

Confidence must be `high`, `medium`, or `low`.

Evidence must cite timestamps, frame numbers, or screenshot references.

## Implementation Agent Prompt Rules

If the user asks for an implementation-agent prompt, generate a tool-agnostic prompt.

The prompt may be used with Codex, Claude Code, Cursor, Windsurf, Aider, OpenHands, OpenClaw agents, or other coding agents.

Do not assume a specific coding agent SDK or API.

The implementation-agent prompt must instruct the agent to:

- Inspect the existing project structure first
- Reuse existing components, routes, styling, and state management
- Implement only the UI behavior visible in the video
- Mark unclear details as TODO
- Avoid inventing hidden functionality
- Use mock data or API placeholders only when necessary
- Run available lint, test, or build checks
- Report changed files, validation results, and unresolved questions

## Quality Checklist

Before finalizing, verify:

- No unsupported feature was invented
- Ambiguous details are marked
- All visible screens are included
- User actions and system responses are separated
- UI elements are grouped clearly
- Implementation notes are scoped to the video
- Sensitive text is not reproduced unnecessarily
