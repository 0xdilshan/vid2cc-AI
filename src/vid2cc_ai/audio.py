import subprocess
import os
import json

def extract_audio(video_path: str, output_path: str):
    """Uses FFmpeg to extract high-quality mono audio for Whisper."""
    command = [
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        "-y", output_path
    ]
    subprocess.run(command, capture_output=True, check=True)

import json

def get_video_codec(video_path: str) -> str:
    """Uses ffprobe to detect the video codec of the input file."""
    command = [
        "ffprobe", "-v", "error", 
        "-select_streams", "v:0", 
        "-show_entries", "stream=codec_name", 
        "-of", "json", 
        video_path
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return data['streams'][0]['codec_name']
    except (subprocess.CalledProcessError, IndexError, KeyError, json.JSONDecodeError):
        # Fallback to h264 if probe fails
        return "h264"

def embed_subtitles(video_path: str, srt_path: str, output_path: str):
    """Soft-embeds SRT as a subtitle track (no re-encoding)."""
    ext = os.path.splitext(output_path)[1].lower()

    command = [
        "ffmpeg", "-i", video_path, "-i", srt_path,
        "-map", "0", 
        "-map", "1:s:0",
        "-c:v", "copy",
        "-c:a", "copy",
    ]

    if ext == ".mp4":
        command.extend(["-c:s", "mov_text"])
    else:
        command.extend(["-c:s", "copy"])

    command.extend(["-y", output_path])
    subprocess.run(command, capture_output=True, check=True)

def hardcode_subtitles(video_path: str, srt_path: str, output_path: str):
    """Burns subtitles directly into the video frames (requires re-encoding)."""
    # The 'subtitles' filter requires escaping backslashes on Windows
    safe_srt_path = srt_path.replace("\\", "/").replace(":", "\\:")
    
    command = [
        "ffmpeg", "-i", video_path,
        "-vf", f"subtitles='{safe_srt_path}'",
        "-c:a", "copy", # Keep original audio
        "-y", output_path
    ]
    subprocess.run(command, capture_output=True, check=True)