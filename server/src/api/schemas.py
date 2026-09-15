from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ConversionStatus(str, Enum):
    UPLOADING = "uploading"
    VALIDATING = "validating"
    CONVERTING = "converting"
    READY = "ready"
    ERROR = "error"


class VideoUploadResponse(BaseModel):
    id: UUID
    filename: str
    format: str
    size: int
    duration: float
    status: ConversionStatus = ConversionStatus.VALIDATING


class ConversionStatusResponse(BaseModel):
    id: UUID
    status: ConversionStatus
    progress: float = Field(ge=0, le=1)
    message: str


class FramesResponse(BaseModel):
    id: UUID
    frames: list[str]
    frame_rate: int = Field(ge=10, le=15)
    width: int = Field(ge=40, le=200)
    height: int = Field(ge=20, le=100)
    duration: float


class AudioTrackResponse(BaseModel):
    id: UUID
    conversion_id: UUID
    format: str
    duration: float


class ErrorResponse(BaseModel):
    error: str
    details: str | None = None
