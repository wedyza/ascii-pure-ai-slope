import asyncio
import io
import logging
import tempfile
import os
from dataclasses import dataclass

import cv2
from PIL import Image

logger = logging.getLogger(__name__)

ASCII_CHARS = "@#S%?*+;:,."
FRAME_WIDTH = 80
FRAME_HEIGHT = 40
TARGET_FPS = 12


@dataclass
class ConversionResult:
    frames: list[str]
    frame_rate: int
    width: int
    height: int
    duration: float


def _luminance_to_char(luminance: int) -> str:
    index = luminance * (len(ASCII_CHARS) - 1) // 255
    return ASCII_CHARS[index]


def frame_to_ascii(image: Image.Image, width: int = FRAME_WIDTH, height: int = FRAME_HEIGHT) -> str:
    image = image.resize((width, height))
    image = image.convert("L")

    pixels = list(image.getdata())
    ascii_chars = [_luminance_to_char(p) for p in pixels]

    lines = []
    for i in range(0, len(ascii_chars), width):
        lines.append("".join(ascii_chars[i : i + width]))

    return "\n".join(lines)


def get_video_duration(video_data: bytes) -> float:
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(video_data)
        tmp_path = tmp.name

    try:
        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cap.release()

        if fps <= 0:
            raise ValueError("Invalid video FPS")

        return frame_count / fps
    finally:
        os.unlink(tmp_path)


async def convert_video_to_ascii(video_data: bytes) -> ConversionResult:
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(video_data)
        tmp_path = tmp.name

    try:
        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps

        frames = []
        frame_interval = max(1, int(fps / TARGET_FPS))
        current_frame = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if current_frame % frame_interval == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_frame)
                ascii_frame = frame_to_ascii(pil_image)
                frames.append(ascii_frame)

            current_frame += 1

        cap.release()

        return ConversionResult(
            frames=frames,
            frame_rate=TARGET_FPS,
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            duration=duration,
        )
    finally:
        os.unlink(tmp_path)
