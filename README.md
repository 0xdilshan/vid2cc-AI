# vid2cc-AI 🎙️🎬

[![PyPI version](https://img.shields.io/pypi/v/vid2cc-ai.svg)](https://pypi.org/project/vid2cc-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
Install directly from the source for development:
```bash
git clone [https://github.com/yourusername/vid2cc-AI.git](https://github.com/yourusername/vid2cc-AI.git)
cd vid2cc-AI
pip install -e .
```

## 📖 How To Use

Once installed, the `vid2cc` command is available globally in your terminal.


---

### Advanced Options

Choose a specific model size (`tiny`, `base`, `small`, `medium`, `large`) to balance speed and accuracy:

```bash
vid2cc input_video.mkv --model medium
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
- [ ] Transcription from YouTube/Vimeo URLs (`yt-dlp`)
- [ ] Embed subtitles into video containers (`--embed`)
- [ ] Burn-in subtitles (`--hardcode`)
- [ ] Multilingual transcription & translation support

## 🛠️ Tech Stack

- **Inference:** OpenAI Whisper
- **Media Engine:** FFmpeg
- **Core:** Python 3.9+, PyTorch
- **CLI Framework:** Argparse

## 📄 License

Distributed under the MIT License.  
See `LICENSE` for more information.