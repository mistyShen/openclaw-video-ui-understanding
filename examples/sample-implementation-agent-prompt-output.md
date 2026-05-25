# Sample Implementation Agent Prompt

Inspect the existing project structure before making changes.

Implementation constraints:

- Reuse existing components, routes, state management, and styling systems.
- Implement only the visible product list, product detail, cart, and success screens.
- Treat exact CTA copy, payment fields, and success headline as TODO items because they are `unable to confirm`.
- Do not invent missing pages, buttons, fields, routes, APIs, states, copy, or behaviors.
- Do not add telemetry.
- Do not call any specific coding-agent SDK or API.

Evidence-backed report summary:

```md
- Confirmed flow: product list -> product detail -> cart -> success.
- Evidence: timestamps `00:00-00:18` and frames `frame_0001.jpg`, `frame_0005.jpg`, `frame_0010.jpg`, `frame_0015.jpg`.
- Confidence values: high / medium / low only.
- Unclear details: exact CTA copy, payment fields, success headline.
```

After implementation:

- Run the project existing lint, test, and build commands.
- Output the modified file list.
- Output verification results.
- Output unresolved `unable to confirm` or `unclear` items.
