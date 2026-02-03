import argparse
import os
from .audio import extract_audio
from .transcriber import Transcriber
from .formatter import save_as_srt

def main():
    parser = argparse.ArgumentParser(description="vid2cc-AI: Video to Subtitles")
    parser.add_argument("input", help="Path to video file")
    parser.add_argument("--model", default="base", help="tiny, base, small, medium, large")
    
    args = parser.parse_args()
    temp_audio = "temp_audio.wav"
    output_srt = os.path.splitext(args.input)[0] + ".srt"

    try:
        print(f"--- Extracting Audio from {args.input} ---")
        extract_audio(args.input, temp_audio)
        
        print(f"--- Transcribing with Whisper ({args.model}) ---")
        ts = Transcriber(args.model)
        segments = ts.transcribe(temp_audio)
        
        save_as_srt(segments, output_srt)
        print(f"DONE! File saved: {output_srt}")
    finally:
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

if __name__ == "__main__":
    main()