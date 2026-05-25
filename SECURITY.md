# Security Policy

## Security Boundary

This project is for local UI video understanding only.

- No third-party upload of videos, frames, screenshots, metadata, or reports.
- No telemetry.
- No credential access.
- Do not read browser passwords, cookies, SSH keys, API keys, or unrelated user directories.
- Do not delete the original video.
- Do not overwrite the original video.
- Do not install dependencies unless the user explicitly agrees.
- Do not automatically modify a codebase.
- Do not automatically publish, send, or exfiltrate analysis results.
- Do not add log upload, remote callback behavior, or remote reporting.
- Do not automatically call paid APIs.
- Do not process private videos over the network by default.

## Sensitive Content Handling

If a video contains passwords, tokens, private messages, personal information, customer data, or other sensitive content, redact those values in any report or prompt.

Uncertain information must be marked as `unable to confirm` or `unclear`. Do not guess.

## Dependencies

- Python >= 3.9 is required.
- `ffmpeg` and `ffprobe` are optional local system dependencies.
- Pillow is optional and only used for contact sheet generation.
- pytest is only used for tests.

This repository must not add OpenCV, moviepy, selenium, playwright, cloud API SDKs, databases, web servers, upload services, telemetry, background services, or browser automation dependencies.

## Reporting Issues

When reporting security issues, do not include private videos, secrets, credentials, or unredacted personal data. Share a minimal reproduction that does not expose sensitive material.
