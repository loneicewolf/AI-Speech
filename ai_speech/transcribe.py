##	OLD VERSION	"""Audio transcription utilities using Whisper."""
##	OLD VERSION	
##	OLD VERSION	from typing import Dict, Any
##	OLD VERSION	
##	OLD VERSION	# Whisper may require heavy compute; using the small model by default.
##	OLD VERSION	import whisper


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# -------------------------------------- #
##	OLD VERSION	## inside transcribe.py
##	OLD VERSION	# MODEL_NAME = "small"
##	OLD VERSION	# MODEL_NAME = "medium" Not tested yet
##	OLD VERSION	MODEL_NAME="medium.en" # ENGLISH ONLY
##	OLD VERSION	# -------------------------------------- #

# copy from the Whisper DOCS

## Available models and languages
# 
# There are six model sizes, four with English-only versions, offering speed and accuracy tradeoffs.
# Below are the names of the available models and their approximate memory requirements and inference speed relative to the large model.
# The relative speeds below are measured by transcribing English speech on a A100, and the real-world speed may vary significantly depending on many factors including the language, the speaking speed, and the available hardware.
# 
# |  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
# |:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
# |  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~10x      |
# |  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~7x       |
# | small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~4x       |
# | medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
# | large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |
# | turbo  |   809 M    |        N/A         |      `turbo`       |     ~6 GB     |      ~8x       |
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# old version
#	def transcribe_audio(audio_path: str) -> Dict[str, Any]:
#	    """Transcribe the given audio file using OpenAI's Whisper.
#	
#	    Args:
#	        audio_path: Path to the WAV file.
#	
#	    Returns:
#	        A dictionary with the transcript text and timestamps.
#	    """
#	    model = whisper.load_model(MODEL_NAME)
#	    result = model.transcribe(audio_path)
#	    return result









"""Audio transcription utilities using Whisper."""

from typing import Dict, Any
import whisper

# Default model (safe fallback)
MODEL_NAME = "medium.en"

def transcribe_audio(audio_path: str, model_name: str = MODEL_NAME) -> Dict[str, Any]:
    """
    Transcribe audio from file using a Whisper model.

    Args:
        audio_path: Path to the audio file (.wav, .mp3, etc.)
        model_name: Which Whisper model to use (tiny, base, small, medium, large)

    Returns:
        The full transcription result dictionary.
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result

