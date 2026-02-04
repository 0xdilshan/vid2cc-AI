import subprocess
import os
import json
import functools

def extract_audio(video_path: str, output_path: str):
    """Uses FFmpeg to extract high-quality mono audio for Whisper."""
    command = [
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        "-y", output_path
    ]
    subprocess.run(command, capture_output=True, check=True)

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
    
@functools.lru_cache(maxsize=None)
def has_encoder(encoder_name: str) -> bool:
    """Checks if the current FFmpeg installation supports a specific encoder."""
    try:
        # Search the list of encoders for the specific name
        result = subprocess.run(
            ["ffmpeg", "-encoders"], 
            capture_output=True, text=True, check=True
        )
        return encoder_name in result.stdout
    except subprocess.CalledProcessError:
        return False

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
    """Burns subtitles with smart codec detection (requires re-encoding)."""
    input_codec = get_video_codec(video_path)
    
    # Logic for AV1
    if input_codec == "av1" and has_encoder("libsvtav1"):
        encoder = "libsvtav1"
        crf = "35"
        preset = "10"
    # Logic for HEVC (x265)
    elif input_codec == "hevc" and has_encoder("libx265"):
        encoder = "libx265"
        crf = "28"
        preset = "veryfast"
    # Fallback to H.264
    else:
        encoder = "libx264"
        crf = "23"
        preset = "veryfast"

    safe_srt = srt_path.replace("\\", "/").replace(":", "\\:")
    
    command = [
        "ffmpeg", "-i", video_path,
        "-vf", f"subtitles='{safe_srt}'",
        "-c:v", encoder,
        "-preset", preset,
        "-crf", crf,
        "-c:a", "copy",
        "-y", output_path
    ]
    
    subprocess.run(command, capture_output=True, check=True)