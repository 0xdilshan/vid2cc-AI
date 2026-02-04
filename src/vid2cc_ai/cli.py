import argparse
import os
from tqdm import tqdm
from .audio import extract_audio, embed_subtitles, hardcode_subtitles
from .transcriber import Transcriber
from .formatter import save_as_srt

def main():
    parser = argparse.ArgumentParser(description="vid2cc-AI: Batch Video Subtitling")
    # Change: nargs='+' allows one or more files
    parser.add_argument("inputs", nargs="+", help="Path to one or more video files")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--embed", action="store_true", help="Soft-embed subtitles")
    parser.add_argument("--hardcode", action="store_true", help="Burn subtitles into video")
    
    args = parser.parse_args()
    
    print(f"--- Initializing Whisper {args.model} model ---")
    ts = Transcriber(args.model)

    # Master progress bar for the batch
    for video_path in tqdm(args.inputs, desc="Overall Batch Progress", unit="file"):
        if not os.path.exists(video_path):
            print(f"Skipping: {video_path} (File not found)")
            continue

        temp_audio = f"temp_{os.path.basename(video_path)}.wav"
        base_name = os.path.splitext(video_path)[0]
        output_srt = base_name + ".srt"

        try:
            extract_audio(video_path, temp_audio)
            
            # Transcription with internal progress (verbose=False triggers Whisper's tqdm)
            segments = ts.transcribe(temp_audio)
            save_as_srt(segments, output_srt)

            if args.embed:
                embed_subtitles(video_path, output_srt, f"{base_name}_embedded.mp4")

            if args.hardcode:
                hardcode_subtitles(video_path, output_srt, f"{base_name}_hardcoded.mp4")

        except Exception as e:
            print(f"Error processing {video_path}: {e}")
        finally:
            if os.path.exists(temp_audio):
                os.remove(temp_audio)

if __name__ == "__main__":
    main()