import subprocess
import os

def extract_audio(video_path: str, output_path: str):
    """Uses FFmpeg to extract high-quality mono audio for Whisper."""
    command = [
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        "-y", output_path
    ]
    subprocess.run(command, capture_output=True, check=True)

def embed_subtitles(video_path: str, srt_path: str, output_path: str):
    """Soft-embeds SRT as a subtitle track (no re-encoding)."""
    # For MP4 we use mov_text, for MKV we can use srt/ass
    ext = os.path.splitext(output_path)[1].lower()
    codec = "mov_text" if ext == ".mp4" else "srt"
    
    command = [
        "ffmpeg", "-i", video_path, "-i", srt_path,
        "-c", "copy", f"-c:s:{0}", codec,
        "-y", output_path
    ]
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