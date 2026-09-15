import asyncio
import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from ..services.audio import extract_audio
from ..services.converter import convert_video_to_ascii, get_video_duration
from ..services.storage import storage
from ..services.validator import validate_upload
from .schemas import (
    ConversionStatus,
    ConversionStatusResponse,
    FramesResponse,
    VideoUploadResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile) -> VideoUploadResponse:
    content = await file.read()

    validation = validate_upload(file.content_type or "", len(content))
    if not validation.valid:
        raise HTTPException(status_code=validation.status_code, detail=validation.error)

    try:
        duration = get_video_duration(content)
    except Exception as e:
        logger.error(f"Failed to get video duration: {e}")
        raise HTTPException(status_code=422, detail="Could not process video file")

    from ..services.validator import validate_duration

    duration_result = validate_duration(duration)
    if not duration_result.valid:
        raise HTTPException(status_code=duration_result.status_code, detail=duration_result.error)

    entry_id = storage.create({
        "filename": file.filename or "unknown",
        "format": file.content_type,
        "size": len(content),
        "duration": duration,
        "status": ConversionStatus.UPLOADING,
        "video_data": content,
    })

    asyncio.create_task(_process_conversion(entry_id, content))

    return VideoUploadResponse(
        id=entry_id,
        filename=file.filename or "unknown",
        format=file.content_type or "",
        size=len(content),
        duration=duration,
        status=ConversionStatus.VALIDATING,
    )


async def _process_conversion(entry_id: UUID, video_data: bytes) -> None:
    try:
        storage.update(entry_id, {"status": ConversionStatus.CONVERTING})

        result = await convert_video_to_ascii(video_data)

        audio_data = extract_audio(video_data)

        storage.update(entry_id, {
            "status": ConversionStatus.READY,
            "frames": result.frames,
            "frame_rate": result.frame_rate,
            "width": result.width,
            "height": result.height,
            "audio_data": audio_data,
        })
    except Exception as e:
        logger.error(f"Conversion failed for {entry_id}: {e}")
        storage.update(entry_id, {"status": ConversionStatus.ERROR, "error": str(e)})


@router.get("/conversion/{id}/status", response_model=ConversionStatusResponse)
async def get_conversion_status(id: UUID) -> ConversionStatusResponse:
    entry = storage.get(id)
    if not entry:
        raise HTTPException(status_code=404, detail="Conversion not found")

    status = entry.get("status", ConversionStatus.UPLOADING)
    progress = 0.0
    message = ""

    if status == ConversionStatus.UPLOADING:
        progress = 0.0
        message = "Uploading video"
    elif status == ConversionStatus.VALIDATING:
        progress = 0.1
        message = "Validating video"
    elif status == ConversionStatus.CONVERTING:
        progress = 0.5
        message = "Converting video to ASCII"
    elif status == ConversionStatus.READY:
        progress = 1.0
        message = "Conversion complete"
    elif status == ConversionStatus.ERROR:
        progress = 0.0
        message = entry.get("error", "Conversion failed")

    return ConversionStatusResponse(
        id=id,
        status=status,
        progress=progress,
        message=message,
    )


@router.get("/conversion/{id}/frames", response_model=FramesResponse)
async def get_conversion_frames(id: UUID) -> FramesResponse:
    entry = storage.get(id)
    if not entry:
        raise HTTPException(status_code=404, detail="Conversion not found")

    if entry.get("status") != ConversionStatus.READY:
        raise HTTPException(status_code=400, detail="Conversion not ready")

    return FramesResponse(
        id=id,
        frames=entry["frames"],
        frame_rate=entry["frame_rate"],
        width=entry["width"],
        height=entry["height"],
        duration=entry["duration"],
    )


@router.get("/conversion/{id}/audio")
async def get_conversion_audio(id: UUID) -> StreamingResponse:
    entry = storage.get(id)
    if not entry:
        raise HTTPException(status_code=404, detail="Conversion not found")

    if entry.get("status") != ConversionStatus.READY:
        raise HTTPException(status_code=400, detail="Conversion not ready")

    audio_data = entry.get("audio_data")
    if not audio_data:
        raise HTTPException(status_code=404, detail="Audio not available")

    return StreamingResponse(
        iter([audio_data]),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline"},
    )


@router.delete("/conversion/{id}")
async def delete_conversion(id: UUID) -> None:
    storage.delete(id)
    return None
