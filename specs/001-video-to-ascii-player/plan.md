# Implementation Plan: Video-to-ASCII Player

**Branch**: `001-video-to-ascii-player` | **Date**: 2026-09-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-video-to-ascii-player/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command; its definition describes the execution workflow.

## Summary

Build a web application that converts uploaded videos (up to 3 minutes) to ASCII art animation while preserving audio. Users upload a video, see conversion progress, then play the ASCII result with synchronized audio. The site supports dark/light themes and prohibits downloading converted content. Backend is Python-based; frontend is a browser-based player.

## Technical Context

**Language/Version**: Python 3.11+ (backend), JavaScript/TypeScript (frontend)

**Primary Dependencies**: FastAPI (backend), OpenCV + Pillow (video-to-ASCII conversion), FFmpeg (audio extraction), React or vanilla JS (frontend player)

**Package Manager**: uv (Python), npm (frontend)

**Linters**: ruff (Python linting/formatting), basedpyright (Python type checking)

**Storage**: N/A (stateless - video processed in memory, not persisted)

**Testing**: pytest (backend), Playwright or Cypress (e2e)

**Target Platform**: Linux/macOS server + modern browsers (Chrome, Firefox, Safari, Edge)

**Project Type**: web-service (frontend + backend)

**Performance Goals**: Convert 3-minute video to ASCII within 60 seconds; maintain AV sync within 100ms during playback

**Constraints**: Stateless (no persistence), no download capability, max 3-minute videos, ~100MB file size limit

**Scale/Scope**: Single-user concurrent sessions; public access without authentication

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Separation of Concerns | PASS | Client/server in separate dirs; client handles UI, server handles conversion |
| II. API Contract First | PASS | REST API for upload/conversion; OpenAPI docs will be generated |
| III. Security Baseline | PASS | Input validation on upload; CORS configured; secrets in .env |
| IV. Error Handling | PASS | Consistent JSON error responses; user-friendly messages client-side |
| V. Testing Strategy | PASS | Unit tests for conversion logic; API integration tests; e2e tests |
| Technical Requirements | PASS | Separate client/server dirs; .env for config; no DB needed (stateless) |
| Development Workflow | PASS | Feature branch; PRs with test passing |

## Project Structure

### Documentation (this feature)

```text
specs/001-video-to-ascii-player/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
server/
├── src/
│   ├── api/
│   │   ├── routes.py          # Upload, conversion, status endpoints
│   │   └── schemas.py         # Request/response models
│   ├── services/
│   │   ├── converter.py       # Video-to-ASCII conversion logic
│   │   ├── audio.py           # Audio extraction
│   │   └── validator.py       # File validation
│   └── main.py                # FastAPI app entry
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── pyproject.toml             # uv dependencies + ruff/basedpyright config
└── .env.example

client/
├── src/
│   ├── components/
│   │   ├── UploadForm.jsx     # Video upload with progress
│   │   ├── ASCIIPlayer.jsx    # ASCII art playback + audio sync
│   │   └── ThemeToggle.jsx    # Dark/light switcher
│   ├── pages/
│   │   └── Home.jsx           # Main page
│   ├── services/
│   │   └── api.js             # Backend API calls
│   └── styles/
│       ├── dark.css
│       └── light.css
├── tests/
├── package.json
└── .env.example
```

**Structure Decision**: Web application with separate `server/` (Python/FastAPI) and `client/` (JavaScript frontend) directories per Constitution Principle I.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations identified. All constitution principles are satisfied by the proposed structure.
