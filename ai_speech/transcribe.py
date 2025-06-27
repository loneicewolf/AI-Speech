"""Audio transcription utilities using Whisper."""

from typing import Dict, Any

# Whisper may require heavy compute; using the small model by default.
import whisper


MODEL_NAME = "small"


def transcribe_audio(audio_path: str) -> Dict[str, Any]:
    """Transcribe the given audio file using OpenAI's Whisper.

    Args:
        audio_path: Path to the WAV file.

    Returns:
        A dictionary with the transcript text and timestamps.
    """
    model = whisper.load_model(MODEL_NAME)
    result = model.transcribe(audio_path)
    return result
