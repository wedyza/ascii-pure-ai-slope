# Research: Video-to-ASCII Player

**Feature**: 001-video-to-ascii-player
**Date**: 2026-09-15

## Decisions

### 1. Video-to-ASCII Conversion Approach

**Decision**: Use pixel-to-character mapping with luminance sampling

**Rationale**: Convert each video frame to grayscale, map pixel brightness to ASCII characters (e.g., `@`, `#`, `*`, `.`, ` `). This is the standard approach for ASCII art conversion and produces recognizable output.

**Alternatives considered**:
- Edge detection only: Rejected - loses color/brightness information, less recognizable
- Color ASCII (ANSI): Rejected - requires terminal support, not browser-compatible

### 2. Audio Handling

**Decision**: Extract audio with FFmpeg, serve as separate stream synchronized client-side

**Rationale**: FFmpeg is the industry standard for audio extraction. Serving audio separately allows browser's native `<audio>` element to handle playback while ASCII frames render independently. Sync achieved via timestamp alignment.

**Alternatives considered**:
- Embed audio in WebSocket stream: Rejected - complex, unnecessary for browser playback
- Convert audio to ASCII beep patterns: Rejected - user requirement is "sound must remain"

### 3. Frame Delivery Strategy

**Decision**: Pre-convert all frames to ASCII on upload, store in memory as JSON array, serve via REST endpoint

**Rationale**: For videos up to 3 minutes at reduced frame rate (10-15 fps), ASCII frame data is manageable in memory (~5-20MB). Pre-conversion avoids real-time processing complexity.

**Alternatives considered**:
- Real-time conversion during playback: Rejected - requires heavy server-side processing per frame
- WebSocket streaming: Rejected - adds complexity; pre-conversion simpler for 3-min limit
- File-based storage: Rejected - violates stateless requirement

### 4. Frontend Framework

**Decision**: Vanilla JavaScript with HTML5 Canvas or pre elements

**Rationale**: Minimal dependencies for a single-page player. Canvas can render ASCII characters efficiently. No build step required for simple UI.

**Alternatives considered**:
- React: Rejected - overkill for single-page app with minimal interactivity
- Three.js: Rejected - 3D rendering unnecessary for 2D ASCII display

### 5. Frame Rate for ASCII Output

**Decision**: 10-15 fps for ASCII output (downsampled from source)

**Rationale**: ASCII art doesn't benefit from high frame rates; 10-15 fps is sufficient for perceived motion while keeping data size manageable. Reduces conversion time and memory usage.

**Alternatives considered**:
- 30 fps: Rejected - 3x data volume with minimal visual improvement
- 5 fps: Rejected - too choppy for smooth playback

### 6. ASCII Character Set

**Decision**: Use gradient of 10-12 characters from dense to sparse

**Rationale**: Standard ASCII density gradient: `@#S%?*+;:,.` provides good visual range. More characters = better detail but diminishing returns beyond 12.

**Alternatives considered**- Binary (2 chars): Rejected - too little detail
- 50+ chars: Rejected - complexity without proportional visual gain

### 7. Theme Implementation

**Decision**: CSS custom properties (variables) with class-based toggling

**Rationale**: CSS variables enable instant theme switching without page reload. Class on `<html>` element switches all colors. Preference stored in `localStorage` for session persistence.

**Alternatives considered**:
- Separate CSS files: Rejected - requires page reload
- Inline styles: Rejected - harder to maintain

## Open Questions

None remaining. All technical decisions resolved.

## Tooling Decisions

### Package Manager

**Decision**: uv for Python dependencies

**Rationale**: uv is significantly faster than pip, handles virtual environments automatically, and has deterministic lockfiles. Modern replacement for pip + venv.

### Linting & Type Checking

**Decision**: ruff (linting/formatting) + basedpyright (type checking)

**Rationale**: ruff is extremely fast Python linter replacing flake8/isort/pylint. basedpyright is a faster, stricter fork of pyright for type checking. Both integrate well with modern Python tooling.

**pyproject.toml config** (reference):
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP"]

[tool.basedpyright]
typeCheckingMode = "standard"
pythonVersion = "3.11"
```
