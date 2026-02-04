import argparse
import os
from tqdm import tqdm
from importlib.metadata import version, PackageNotFoundError
from .audio import extract_audio, embed_subtitles, hardcode_subtitles
from .transcriber import Transcriber
from .formatter import save_as_srt

def main():

    try:
        __version__ = version("vid2cc-ai")
    except PackageNotFoundError:
        __version__ = "unknown"

    parser = argparse.ArgumentParser(description="vid2cc-AI: Batch Video Subtitling")
    parser.add_argument("inputs", nargs="+", help="Path to one or more video files")
    parser.add_argument("-m", "--model", default="base", choices=["tiny", "base", "small", "medium", "large", "turbo"])
    parser.add_argument("--embed", action="store_true", help="Soft-embed subtitles")
    parser.add_argument("--hardcode", action="store_true", help="Burn subtitles into video")
    parser.add_argument("-o", "--output-dir", help="Directory to save all generated files")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    # Create output directory if specified
    if args.output_dir and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    print(f"--- Initializing Whisper {args.model} model ---")
    ts = Transcriber(args.model)

    for video_path in tqdm(args.inputs, desc="Overall Batch Progress", unit="file"):
        if not os.path.exists(video_path):
            print(f"Skipping: {video_path} (File not found)")
            continue

        # Get the filename without extension for naming outputs
        file_base = os.path.splitext(os.path.basename(video_path))[0]
        
        # Route outputs to output_dir if provided, else keep next to source
        target_dir = args.output_dir if args.output_dir else os.path.dirname(video_path)
        
        temp_audio = os.path.join(target_dir, f"temp_{file_base}.wav")
        output_srt = os.path.join(target_dir, f"{file_base}.srt")

        try:
            extract_audio(video_path, temp_audio)
            
            segments = ts.transcribe(temp_audio)
            save_as_srt(segments, output_srt)

            if args.embed:
                out_v = os.path.join(target_dir, f"{file_base}_embedded.mp4")
                embed_subtitles(video_path, output_srt, out_v)

            if args.hardcode:
                out_v = os.path.join(target_dir, f"{file_base}_hardcoded.mp4")
                hardcode_subtitles(video_path, output_srt, out_v)

        except Exception as e:
            print(f"Error processing {video_path}: {e}")
        finally:
            if os.path.exists(temp_audio):
                os.remove(temp_audio)

if __name__ == "__main__":
    main()