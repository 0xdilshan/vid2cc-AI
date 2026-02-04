# vid2cc-AI 🎙️🎬

[![PyPI version](https://img.shields.io/pypi/v/vid2cc-ai.svg)](https://pypi.org/project/vid2cc-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![CI Status](https://github.com/0xdilshan/vid2cc-AI/actions/workflows/ci.yml/badge.svg)

**vid2cc-AI** is a high-performance CLI tool designed to bridge the gap between raw video and accessible content. By leveraging OpenAI's Whisper models and FFmpeg's robust media handling, it automates the creation of perfectly synced `.srt` subtitles.

---

## 🚀 Key Features

- **AI-Driven Transcription:** Powered by OpenAI Whisper for industry-leading accuracy.
- **Hardware Acceleration:** Automatic CUDA detection for GPU-accelerated processing.
- **Intelligent Pre-processing:** FFmpeg-based audio extraction optimized for speech recognition (16kHz Mono).
- **Professional Packaging:** Fully installable via pip with a dedicated command-line entry point.

---

## ⚙️ Installation

### 1. Prerequisite: FFmpeg
This tool requires FFmpeg to be installed on your system.
- **macOS:** `brew install ffmpeg`
- **Windows:** `choco install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

### 2. Install vid2cc-AI

```bash
pip install vid2cc-ai
```

 **Install directly from the source for development:*
```bash
git clone https://github.com/0xdilshan/vid2cc-AI.git
cd vid2cc-AI
pip install -e .
```

## 📖 How To Use

Once installed, the `vid2cc` command is available globally in your terminal.

#### Examples

*For maximum accuracy with toggleable subs:*

```bash
vid2cc example.mp4 --model large --embed
```

---

### 🛠️ Advanced Options

Fine-tune your output using the following flags:

| Flag | Description |
| :--- | :--- |
| `--model [size]` | Choose Whisper model: `tiny`, `base`, `small`, `medium`, `large` or `turbo`. |
| `--embed` | **Soft Subtitles:** Adds the SRT as a metadata track. Fast and allows users to toggle subtitles on/off in players like VLC. |
| `--hardcode` | **Burn-in Subtitles:** Permanently draws subtitles onto the video. Essential for social media (Instagram/TikTok) where players don't support SRT files. |

### 📦 Batch Processing
No need to run the command for every single file. You can pass multiple videos at once:

```bash
# Process all mp4 files in the current directory
vid2cc *.mp4 --model small --embed

# Process multiple specific files
vid2cc video1.mp4 video2.mkv video3.mov --model base --embed
```

## 📦 Usage as a Library

You can integrate **vid2cc-AI** directly into your Python projects:

```python
from vid2cc_ai import Transcriber, extract_audio

# Extract and Transcribe
extract_audio("video.mp4", "audio.wav")
ts = Transcriber("base")
segments = ts.transcribe("audio.wav")

for s in segments:
    print(f"[{s['start']:.2f}s] {s['text']}")
```


---

### 🧪 Testing


```bash
# Install test dependencies
pip install pytest

# Run the test suite
pytest
```


---

## 🗺️ Roadmap

- [x] Local video → SRT transcription
- [x] Embed subtitles into video containers (`--embed`)
- [x] Burn-in subtitles (`--hardcode`)
- [ ] Multilingual transcription & translation support
- [ ] Transcription from YouTube/Vimeo URLs (`yt-dlp`)

## 🛠️ Tech Stack

- **Inference:** OpenAI Whisper
- **Media Engine:** FFmpeg
- **Core:** Python 3.9+, PyTorch
- **CLI Framework:** Argparse

## 📄 License

Distributed under the MIT License.  
See `LICENSE` for more information.