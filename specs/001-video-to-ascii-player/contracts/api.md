# API Contract: Video-to-ASCII Player

**Base URL**: `/api/v1`

## Endpoints

### POST /upload

Upload a video file for conversion to ASCII.

**Request**:
- Content-Type: multipart/form-data
- Body: `file` (binary video file)

**Response** (201 Created):
```json
{
  "id": "uuid-string",
  "filename": "video.mp4",
  "format": "video/mp4",
  "size": 10485760,
  "duration": 45.2,
  "status": "validating"
}
```

**Error Responses**:
- 400: `{"error": "Invalid file format. Supported: MP4, WebM, AVI, MOV"}`
- 413: `{"error": "File too large. Maximum size: 100MB"}`
- 422: `{"error": "Video duration exceeds 3-minute limit"}`

---

### GET /conversion/{id}/status

Check conversion progress.

**Response** (200 OK):
```json
{
  "id": "uuid-string",
  "status": "converting",
  "progress": 0.65,
  "message": "Converting frame 975 of 1500"
}
```

**Status values**: `uploading`, `validating`, `converting`, `ready`, `error`

---

### GET /conversion/{id}/frames

Get all ASCII frames for playback.

**Response** (200 OK):
```json
{
  "id": "uuid-string",
  "frames": [
    "                        ",
    "    @@##%%  %%##@@      ",
    "   @@######%%##@@       "
  ],
  "frame_rate": 12,
  "width": 80,
  "height": 40,
  "duration": 45.2
}
```

**Notes**:
- Each frame is a string of ASCII characters
- Frames are ordered chronologically
- Client renders frames sequentially at specified frame_rate
- `id` is a temporary UUID for in-memory session tracking

---

### GET /conversion/{id}/audio

Stream the extracted audio.

**Response** (200 OK):
- Content-Type: audio/mpeg (or original audio format)
- Body: Binary audio stream

**Notes**:
- `id` is a temporary UUID for in-memory session tracking
- Server auto-cleans after 5-minute TTL
- Client should call DELETE on page unload for immediate cleanup

---

### DELETE /conversion/{id}

Explicitly clean up conversion data (optional, for stateless design).

**Response** (204 No Content)

**Notes**:
- Supports Range requests for seeking
- Client uses HTML5 `<audio>` element for playback
- Audio stream tied to temporary UUID session

---

## CORS Configuration

- Allowed origins: Configurable via `ALLOWED_ORIGINS` env var
- Allowed methods: GET, POST, DELETE
- Allowed headers: Content-Type
- Credentials: Not supported (stateless, no auth)

## Rate Limiting

- Upload endpoint: 5 requests per minute per IP
- Other endpoints: 60 requests per minute per IP

## Error Response Format

All errors follow consistent structure:
```json
{
  "error": "Human-readable error message",
  "details": "Optional technical details (dev mode only)"
}
```
