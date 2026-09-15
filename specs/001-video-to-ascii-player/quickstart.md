# Quickstart Validation Guide: Video-to-ASCII Player

**Feature**: 001-video-to-ascii-player
**Date**: 2026-09-15

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed (for client)
- FFmpeg installed and in PATH
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Setup

```bash
# Clone and navigate to project
cd podsite

# Setup backend
cd server
uv sync                    # Install dependencies via uv

# Setup frontend
cd ../client
npm install
```

## Configuration

Create `server/.env`:
```
ALLOWED_ORIGINS=http://localhost:3000
MAX_UPLOAD_SIZE=104857600
MAX_DURATION=180
```

Create `client/.env`:
```
VITE_API_URL=http://localhost:8000
```

## Run Servers

```bash
# Terminal 1: Backend
cd server
uv run uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd client
npm run dev -- --port 3000
```

## Linting & Type Checking

```bash
# Run ruff linter + formatter
uv run ruff check .
uv run ruff format .

# Run basedpyright type checker
uv run basedpyright
```

## Validation Scenarios

### Scenario 1: Upload and Convert Video

**Steps**:
1. Open browser to `http://localhost:3000`
2. Click upload area or drag video file (MP4, <3 min)
3. Observe progress indicator during conversion
4. Verify player appears after conversion completes

**Expected**: Upload completes within 60 seconds for 3-minute video; progress bar updates; player visible with ASCII content

---

### Scenario 2: Play ASCII Video with Audio

**Steps**:
1. After conversion, click Play button
2. Listen for audio playback
3. Observe ASCII frames animating
4. Click Pause, verify both pause
5. Seek to different position, verify sync

**Expected**: Audio and ASCII animation play in sync; controls responsive; seeking works without desync

---

### Scenario 3: Theme Switching

**Steps**:
1. Click theme toggle button
2. Verify colors change (dark ↔ light)
3. Navigate away and back
4. Verify theme persists

**Expected**: Instant visual change; theme persists during session; default is dark

---

### Scenario 4: File Validation

**Steps**:
1. Try uploading .txt file
2. Try uploading video >3 minutes
3. Try uploading >100MB file

**Expected**: Clear error messages for each; no conversion attempted

---

### Scenario 5: No Download Capability

**Steps**:
1. After conversion, inspect page (F12)
2. Check Network tab for file URLs
3. Right-click on player area
4. Look for save/download options

**Expected**: No download links; no save option; no file endpoints in network tab

---

### Scenario 6: API Contract Validation

**Steps**:
```bash
# Upload test
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@test-video.mp4"

# Check status
curl http://localhost:8000/api/v1/conversion/{id}/status

# Get frames
curl http://localhost:8000/api/v1/conversion/{id}/frames

# Get audio
curl http://localhost:8000/api/v1/conversion/{id}/audio
```

**Expected**: All endpoints return correct JSON/audio; error responses follow contract format

---

## Performance Validation

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Upload + convert time | <60s for 3-min video | Timer from upload to player ready |
| AV sync | <100ms drift | Manual check: clap at start, compare audio/visual |
| Memory usage | <500MB per conversion | Monitor server process during conversion |

## Troubleshooting

- **FFmpeg not found**: Ensure FFmpeg is installed and in system PATH
- **CORS errors**: Check `ALLOWED_ORIGINS` in server `.env`
- **Upload fails**: Verify `MAX_UPLOAD_SIZE` is sufficient
- **Audio not playing**: Check browser supports audio format (convert to mp3 if needed)
