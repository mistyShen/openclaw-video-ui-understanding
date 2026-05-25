# Implementation Agent Prompt

Use this only after completing `templates/ui-understanding-output.md`.

## Prompt

Inspect the existing project structure before making changes.

Implementation constraints:

- Reuse existing components, routes, state management, and styling systems.
- Implement only functionality clearly visible in the video-backed UI understanding report.
- Treat any `unable to confirm` or `unclear` detail as a TODO; do not invent missing pages, buttons, fields, routes, APIs, states, copy, or behaviors.
- Preserve all evidence and confidence notes from the report.
- Do not add telemetry.
- Do not upload video, frames, screenshots, metadata, or reports.
- Do not automatically publish, send, or exfiltrate analysis results.
- Do not read browser passwords, cookies, SSH keys, API keys, or unrelated user directories.
- Do not call any specific coding-agent SDK or API.

Video-backed UI understanding report:

```md
[Paste the completed UI understanding report here.]
```

After implementation:

- Run the project existing lint, test, and build commands.
- Output the modified file list.
- Output verification results.
- Output unresolved `unable to confirm` or `unclear` items.
