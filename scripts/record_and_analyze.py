#!/usr/bin/env python3
"""CLI to record audio or transcribe existing file, analyze, and provide tips."""

import argparse
from pathlib import Path

from ai_speech.recorder import record_audio
from ai_speech.transcribe import transcribe_audio
from ai_speech.analyzer import analyze_disfluencies
from ai_speech.tips import generate_tips


def main() -> None:
    parser = argparse.ArgumentParser(description="Record or analyze existing speech")
    parser.add_argument(
        "--duration", type=int, help="Recording duration in seconds (if recording)"
    )
    parser.add_argument(
        "--outfile", type=Path, default=Path("recording.wav"),
        help="Output WAV filename when recording"
    )
    parser.add_argument(
        "--inputfile", type=Path,
        help="Optional: Path to existing .mp3/.wav file to analyze"
    )

    args = parser.parse_args()

    if args.inputfile:
        # Skip recording, use existing file
        audio_path = args.inputfile
        if not audio_path.exists():
            print(f" Error: file {audio_path} not found.")
            return
        print(f" Using existing file: {audio_path}")
    elif args.duration:
        # Record from mic
        print(f" Recording {args.duration} seconds of audio...")
        audio_path = record_audio(str(args.outfile), duration=args.duration)
        print(f" Audio saved to {args.outfile}")
    else:
        print(" Error: You must provide either --inputfile or --duration.")
        return

    # Transcribe
    transcript = transcribe_audio(str(audio_path))
    print("\n=== Transcript ===")
    print(transcript.get("text", ""))

    # Analyze
    metrics = analyze_disfluencies(transcript.get("segments", []))
    print("\n=== Analysis ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # Tips
    tips = generate_tips(metrics)
    print("\n=== Tips ===")
    for tip in tips:
        print(f"- {tip}")


if __name__ == "__main__":
    main()
