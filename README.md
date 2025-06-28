# AI-Speech
A simple toolkit for recording your speech, transcribing it with [Whisper](https://github.com/openai/whisper), analyzing common disfluencies, and generating tips to improve fluency. It is intended as an experimental learning project and **not** a replacement for professional therapy.

## Quick installation

Use the following commands for a fresh setup:

```bash
python3 -m venv AI_VENV
source AI_VENV/bin/activate
git clone https://github.com/loneicewolf/AI-Speech
cd AI-Speech
pip install -U openai-whisper
# I have GPU PassTrough with VM + NVIDIA + VFIO so i have to
# sudo modprobe -r vfio_pci && echo "MODPROBE removing VIO_PCI OK" ; sleep 2; sudo modprobe nvidia

# this is how I do it
# PYTHONPATH=. python scripts/record_and_analyze.py --duration 3 --outfile my_recording.wav
```

Then install the remaining dependencies:

```bash
pip install -r requirements.txt
```

The `whisper` package requires PyTorch. Refer to the [Whisper documentation](https://github.com/openai/whisper) for setup instructions.

## Usage

Record and analyze your speech from the command line:

```bash
python scripts/record_and_analyze.py --duration 10 --outfile my_recording.wav
```

The program will record audio, transcribe it, analyze for filler words and repetitions, and provide suggestions.

## Disclaimer

This project is for educational purposes. The tips generated are not medical advice. For professional help, consult a qualified speech-language pathologist.
