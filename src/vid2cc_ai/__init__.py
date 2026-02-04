# src/vid2cc_ai/__init__.py
from importlib.metadata import version, PackageNotFoundError
from .transcriber import Transcriber
from .audio import extract_audio, embed_subtitles, hardcode_subtitles
from .formatter import save_as_srt

try:
    __version__ = version("vid2cc-ai")
except PackageNotFoundError:
    # Fallback if the package is not installed
    __version__ = "unknown"