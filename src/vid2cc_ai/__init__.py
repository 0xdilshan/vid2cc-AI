# src/vid2cc_ai/__init__.py
from .transcriber import Transcriber
from .audio import extract_audio, embed_subtitles, hardcode_subtitles
from .formatter import save_as_srt

__version__ = "0.1.0"