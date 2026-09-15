import logging
import os
import shutil
import subprocess
import tempfile

logger = logging.getLogger(__name__)


def _find_ffmpeg() -> str | None:
    return shutil.which("ffmpeg")


def extract_audio(video_data: bytes) -> bytes | None:
    ffmpeg = _find_ffmpeg()
    if not ffmpeg:
        logger.warning("ffmpeg not found, skipping audio extraction")
        return None

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_tmp:
        video_tmp.write(video_data)
        video_path = video_tmp.name

    audio_path = video_path + ".mp3"

    try:
        cmd = [
            ffmpeg, "-i", video_path,
            "-vn", "-acodec", "libmp3lame", "-q:a", "2",
            "-y", audio_path,
        ]
        subprocess.run(cmd, capture_output=True, check=True)

        with open(audio_path, "rb") as f:
            return f.read()
    except Exception as e:
        logger.warning(f"Audio extraction failed: {e}")
        return None
    finally:
        if os.path.exists(video_path):
            os.unlink(video_path)
        if os.path.exists(audio_path):
            os.unlink(audio_path)
