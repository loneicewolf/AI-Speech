"""Generate tips based on analysis results."""

from typing import Dict, List

DISCLAIMER = (
    "The following tips are generated automatically and do not constitute\n"
    "medical advice. For professional evaluation, consult a qualified\n"
    "speech-language pathologist."
)


def generate_tips(metrics: Dict[str, int]) -> List[str]:
    """Create user-friendly tips from analyzer metrics."""
    tips = [DISCLAIMER]

    if metrics.get("filler_words", 0) > 3:
        tips.append(
            "Try to pause briefly instead of using filler words like 'um' or 'uh'."
        )

    if metrics.get("repetitions", 0) > 0:
        tips.append("Focus on slowing down to avoid repeating words.")

    word_count = metrics.get("word_count", 1)
    if word_count / (metrics.get("repetitions", 0) + 1) < 5:
        tips.append("Practice speaking with longer sentences to build fluency.")

    return tips
