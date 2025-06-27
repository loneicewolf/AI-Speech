#!/usr/bin/env python3
"""CLI to record audio, transcribe, analyze, and provide tips."""

import argparse
from pathlib import Path

from ai_speech.recorder import record_audio
from ai_speech.transcribe import transcribe_audio
from ai_speech.analyzer import analyze_disfluencies
from ai_speech.tips import generate_tips


def main() -> None:
    parser = argparse.ArgumentParser(description="Record and analyze speech")
    parser.add_argument(
        "--duration", type=int, default=5, help="Recording duration in seconds"
    )
    parser.add_argument(
        "--outfile",
        type=Path,
        default=Path("recording.wav"),
        help="Output WAV filename",
    )
    args = parser.parse_args()

    wav_path = record_audio(str(args.outfile), duration=args.duration)
    transcript = transcribe_audio(wav_path)
    metrics = analyze_disfluencies(transcript.get("segments", []))
    tips = generate_tips(metrics)

    print("\n=== Transcript ===")
    print(transcript.get("text", ""))
    print("\n=== Analysis ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\n=== Tips ===")
    for tip in tips:
        print(f"- {tip}")


if __name__ == "__main__":
    main()
