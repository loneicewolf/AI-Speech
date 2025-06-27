"""Analyze transcripts for disfluencies."""

from typing import List, Dict

FILLER_WORDS = {"um", "uh", "like", "you know"}


def analyze_disfluencies(transcript: List[Dict]) -> Dict[str, int]:
    """Analyze tokens from a Whisper transcript for disfluencies.

    Args:
        transcript: List of segments from Whisper. Each segment contains 'text'.

    Returns:
        Counts of filler words and repetitions.
    """
    text = " ".join(seg["text"] for seg in transcript)
    words = text.lower().split()
    filler_count = sum(1 for word in words if word in FILLER_WORDS)

    repetitions = 0
    prev_word = None
    for word in words:
        if word == prev_word:
            repetitions += 1
        prev_word = word

    return {
        "filler_words": filler_count,
        "repetitions": repetitions,
        "word_count": len(words),
    }
