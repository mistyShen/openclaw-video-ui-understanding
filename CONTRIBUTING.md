# Contributing

## Scope

Contributions should stay focused on local video-based UI understanding for OpenClaw skill usage.

Do not add:

- Telemetry
- Third-party upload workflows
- Automatic code modification
- Automatic deletion or overwriting of original videos
- Unrelated media-processing features

## Development

1. Use Python 3.9+.
2. Keep scripts runnable as standalone Python scripts.
3. Keep `ffmpeg` and `ffprobe` optional.
4. Keep Pillow optional and documented.
5. Preserve the requirement that unclear UI details must be marked as `无法确认`.

## Testing

Run:

```bash
python3 -m pytest
```

Tests are intentionally lightweight and should pass without `ffmpeg`, `ffprobe`, or Pillow.

## Pull Request Expectations

- Update documentation when behavior changes.
- Add or adjust tests when scripts change.
- Keep outputs conservative and evidence-based.
- Avoid adding new dependencies without a strong reason.
