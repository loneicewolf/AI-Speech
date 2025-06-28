#!/usr/bin/env python3
"""Record or transcribe, then post-process with selectable actions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_speech.recorder import record_audio
from ai_speech.transcribe import transcribe_audio
from ai_speech.analyzer import analyze_disfluencies
from ai_speech.tips import generate_tips
from ai_speech.actions import run_action_mode

DEFAULT_MODEL = "medium.en"

def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI-Speech pipeline: record / transcribe / actions / tips"
    )

    # Input options
    parser.add_argument("--duration", type=int, help="Record N seconds from mic")
    parser.add_argument("--outfile", type=Path, default=Path("recording.wav"))
    parser.add_argument("--inputfile", type=Path, help="Existing .mp3/.wav to analyse")
    
    # Aes
    parser.add_argument(
    "--aeskey", type=str,
    help="Optional 16/24/32-byte key for AES encryption (used with --action 2 or 3)"
    )


    # Whisper knob
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Whisper model (tiny|base|small|medium|large etc.)")

    # Post-processing
    parser.add_argument("--action", type=int, choices=range(1, 5),
                        help="Action mode 1-4 (see --help)")
    parser.add_argument("--saveoutput", type=Path,
                        help="Write final result (transcript or action) to file")

    args = parser.parse_args()

    # 1) Get audio path
    if args.inputfile:
        audio_path = args.inputfile
        if not audio_path.exists():
            raise SystemExit(f"❌  File not found: {audio_path}")
        print(f"🎧  Using existing file: {audio_path}")
    elif args.duration:
        print(f"🎙️  Recording {args.duration}s …")
        audio_path = record_audio(str(args.outfile), duration=args.duration)
    else:
        raise SystemExit("⚠️  Provide --inputfile OR --duration.")

    # 2) Transcribe
    transcript = transcribe_audio(str(audio_path), model_name=args.model)

    # 3) If --action chosen, run & quit
    
    #if args.action:
    #    result = run_action_mode(transcript, mode=args.action)
    #    print(f"\n=== 🎯 Action {args.action} ===\n{result}")
    #    if args.saveoutput:
    #        args.saveoutput.write_text(result)
    #        print(f"✅  Saved to {args.saveoutput}")
    #    return
    
    # 3) If --action chosen, run & quit
    if args.action:
        kwargs = {}
        if args.aeskey:
            ##key = args.aeskey.encode("utf-8")
            ##if len(key) not in (16, 24, 32):
            ##    raise ValueError("AES key must be 16, 24, or 32 bytes long")
            ##kwargs["key"] = key
            import base64
            try:
                key = base64.b64decode(args.aeskey)
                if len(key) not in (16, 24, 32):
                    raise ValueError
            except Exception:
                raise ValueError("AES key must be base64-encoded and decode to 16, 24, or 32 bytes")
            kwargs["key"] = key


        result = run_action_mode(transcript, mode=args.action, **kwargs)
        print(f"\n=== 🎯 Action {args.action} ===\n{result}")
        if args.saveoutput:
            args.saveoutput.write_text(result)
            print(f"✅  Saved to {args.saveoutput}")
        return


    # 4) Full analysis branch
    print("\n=== 📝 Transcript ===\n", transcript.get("text", ""))
    metrics = analyze_disfluencies(transcript.get("segments", []))
    print("\n=== 🔍 Analysis ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    tips = generate_tips(metrics)
    print("\n=== 💡 Tips ===")
    for tip in tips:
        print(f"- {tip}")

    # 5) Optional dump
    if args.saveoutput:
        args.saveoutput.write_text(json.dumps(
            {"transcript": transcript, "metrics": metrics, "tips": tips},
            indent=2, ensure_ascii=False))
        print(f"✅  Saved JSON to {args.saveoutput}")

if __name__ == "__main__":
    main()
