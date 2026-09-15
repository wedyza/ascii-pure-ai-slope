# Data Model: Video-to-ASCII Player

**Feature**: 001-video-to-ascii-player
**Date**: 2026-09-15

## Entities

### VideoUpload

Represents a video file submitted by the user for conversion.

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique identifier for this upload session |
| filename | string | Original filename submitted by user |
| format | string | MIME type (video/mp4, video/webm, etc.) |
| size | integer | File size in bytes |
| duration | float | Video duration in seconds (max 180) |
| status | enum | `uploading` \| `validating` \| `converting` \| `ready` \| `error` |
| created_at | datetime | Upload initiation timestamp |

**Validation rules**:
- Format MUST be one of: video/mp4, video/webm, video/avi, video/quicktime
- Size MUST NOT exceed 100MB (104,857,600 bytes)
- Duration MUST NOT exceed 180 seconds (3 minutes)

**State transitions**:
```
uploading → validating → converting → ready
                  ↓            ↓
                error        error
```

### ASCIIConversion

Represents the converted ASCII frame data and associated audio.

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique identifier for conversion result |
| upload_id | string (UUID) | Reference to VideoUpload |
| frames | array[string] | ASCII art frames (one string per frame) |
| frame_rate | integer | Frames per second (10-15) |
| width | integer | ASCII width in characters |
| height | integer | ASCII height in characters |
| audio_url | string | URL to extracted audio stream |
| duration | float | Total duration in seconds |
| created_at | datetime | Conversion completion timestamp |

**Validation rules**:
- frames array length MUST equal duration × frame_rate
- width MUST be between 40 and 200 characters
- height MUST be between 20 and 100 characters

### AudioTrack

Represents extracted audio from the original video.

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique identifier |
| conversion_id | string (UUID) | Reference to ASCIIConversion |
| format | string | Audio format (audio/mpeg, audio/ogg, etc.) |
| duration | float | Duration in seconds |
| stream_url | string | URL to audio stream endpoint |

### Theme

Client-side theme preference (not persisted server-side).

| Field | Type | Description |
|-------|------|-------------|
| mode | enum | `dark` \| `light` |
| persisted | boolean | Whether stored in localStorage |

**Default**: `dark` when no preference exists.

## Relationships

```
VideoUpload 1 ──── 1 ASCIIConversion
ASCIIConversion 1 ──── 1 AudioTrack
```

## In-Memory Storage Pattern

Since the system is stateless, entities exist only during the conversion session:

1. **Upload phase**: VideoUpload created in memory, keyed by UUID
2. **Conversion phase**: ASCIIConversion + AudioTrack created in memory, linked by UUID
3. **Playback phase**: Client fetches frames + audio via API using UUID
4. **Session end**: All data garbage collected (TTL expiry or explicit DELETE)

**UUID Purpose**: Temporary in-memory keys to correlate upload → conversion → playback within a session. No database required. Memory management via TTL (time-to-live) on conversion objects (default: 5 minutes).
