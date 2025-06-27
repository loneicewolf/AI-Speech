"""Audio recording utilities."""

import sounddevice as sd
import soundfile as sf
from typing import Optional


def record_audio(filename: str, duration: int = 5, samplerate: int = 16000, channels: int = 1) -> str:
    """Record audio from the microphone and save to a WAV file.

    Args:
        filename: Path where the recording will be saved.
        duration: Recording duration in seconds.
        samplerate: Sample rate for recording.
        channels: Number of microphone channels.

    Returns:
        The path to the saved WAV file.
    """
    print(f"Recording {duration} seconds of audio...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
    sd.wait()  # Wait until recording is finished
    sf.write(filename, recording, samplerate)
    print(f"Audio saved to {filename}")
    return filename
