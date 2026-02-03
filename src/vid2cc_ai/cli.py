import argparse
import os
from .audio import extract_audio, embed_subtitles, hardcode_subtitles
from .transcriber import Transcriber
from .formatter import save_as_srt

def main():
    parser = argparse.ArgumentParser(description="vid2cc-AI: Video to Subtitles")
    parser.add_argument("input", help="Path to video file")
    parser.add_argument("--model", default="base", help="tiny, base, small, medium, large")
    parser.add_argument("--embed", action="store_true", help="Soft-embed subtitles into a new video file")
    parser.add_argument("--hardcode", action="store_true", help="Burn subtitles into the video (re-encodes)")
    
    args = parser.parse_args()
    temp_audio = "temp_audio.wav"
    base_name = os.path.splitext(args.input)[0]
    output_srt = base_name + ".srt"

    try:
        print(f"--- Extracting Audio from {args.input} ---")
        extract_audio(args.input, temp_audio)
        
        print(f"--- Transcribing with Whisper ({args.model}) ---")
        ts = Transcriber(args.model)
        segments = ts.transcribe(temp_audio)
        
        save_as_srt(segments, output_srt)
        print(f"SRT saved: {output_srt}")

        if args.embed:
            out_v = f"{base_name}_embedded.mp4"
            print(f"--- Embedding Subtitles into {out_v} ---")
            embed_subtitles(args.input, output_srt, out_v)
            print(f"DONE! Embedded video: {out_v}")

        if args.hardcode:
            out_v = f"{base_name}_hardcoded.mp4"
            print(f"--- Hardcoding Subtitles into {out_v} (This may take a while) ---")
            hardcode_subtitles(args.input, output_srt, out_v)
            print(f"DONE! Hardcoded video: {out_v}")

    finally:
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

if __name__ == "__main__":
    main()