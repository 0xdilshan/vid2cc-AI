# FFMPEG Installation Guide

**vid2cc-AI** requires **FFmpeg** to be installed and added to your system's `PATH`.  
FFmpeg handles all audio extraction and subtitle embedding tasks.

---

## 🍎 macOS

The easiest way to install FFmpeg on macOS is via **Homebrew**:

```bash
brew install ffmpeg
```

---

## 🪟 Windows

Choose one of the following modern package managers.

**Using Winget (recommended):**
```powershell
winget install Gyan.FFmpeg
```

**Using Chocolatey:**
```powershell
choco install ffmpeg
```

---

## 🐧 Linux

Use the command that matches your distribution.

| Distribution        | Command |
|---------------------|---------|
| Ubuntu / Debian     | `sudo apt update && sudo apt install ffmpeg` |
| Fedora              | `sudo dnf install ffmpeg` |
| Arch Linux          | `sudo pacman -S ffmpeg` |
| Universal (Snap)    | `sudo snap install ffmpeg` |
