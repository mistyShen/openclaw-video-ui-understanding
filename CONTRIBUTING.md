# Contributing

## Scope

Contributions should stay focused on local video-based UI understanding for OpenClaw skill usage.

Do not add:

- Telemetry
- Third-party upload workflows
- Automatic code modification
- Automatic deletion or overwriting of original videos
- Browser automation dependencies
- Coding-agent SDK calls
- Unrelated media-processing features

## Development

1. Use Python 3.9 or newer.
2. Keep scripts runnable as standalone Python scripts.
3. Keep `ffmpeg` and `ffprobe` optional.
4. Keep Pillow optional and documented.
5. Preserve the requirement that unclear UI details must be marked as `unable to confirm` or `unclear`.

## Testing

Run:

```bash
python3 -m pytest tests
```

Tests are intentionally lightweight and should pass without `ffmpeg`, `ffprobe`, or Pillow.

## Pull Request Expectations

- Update documentation when behavior changes
- Add or adjust tests when scripts change
- Keep outputs conservative and evidence-based
- Avoid adding dependencies without a strong reason
