# 📦 AI-SPEECH REPO OVERVIEW — STRUCTURE & COMPONENTS

This document explains the contents of the current AI-SPEECH repo, without referencing experimental or off-topic discussion. It lists what exists, what it does, and what parts are important for core functionality.

---

## 📁 Folder & File Overview

```
./scripts/record_and_analyze.py        # Main CLI tool to record/transcribe/analyze
./scripts/                             # Place for CLI scripts and helper modules

./media_files/                         # Folder for WAV/MP3 input files (e.g. from mic or external)

./ai_speech/transcribe.py              # Core Whisper wrapper for transcription
./ai_speech/analyzer.py                # Disfluency analysis (repetition, filler words)
./ai_speech/actions.py                 # Post-processing actions: encrypt, scan keywords, etc.
./ai_speech/recorder.py                # Records from microphone into a .wav
./ai_speech/tips.py                    # Generates general speech improvement tips
./ai_speech/__init__.py                # Initializes the ai_speech module

./README.md                            # Main readme
./EXAMPLES.md                          # All supported CLI examples
./PROBLEMS_and_PROGRESS.md             # Ongoing notes, bugs, milestones
./requirements.txt                     # Python dependencies
```

---

## 🧩 Key Components

### 🔹 `record_and_analyze.py`

* Entry-point for the system
* Supports:

  * Recording via mic (`--duration`)
  * Analyzing existing audio (`--inputfile`)
  * Running extra actions (`--action`)
  * Encrypting output
  * Saving JSON/text results

### 🔹 `transcribe.py`

* Loads Whisper model
* Supports various decoding params like `temperature`, `logprob_threshold`, etc.
* Word-level timestamps are enabled

### 🔹 `analyzer.py`

* Analyzes the transcript for common disfluencies:

  * Word repetition
  * Filler usage

### 🔹 `actions.py`

* Handles actions:

  * Base64 / AES encryption
  * Reverse encryption
  * Keyword search from `keywords.txt`
  * Runs single-mode or full-action suite

### 🔹 `tips.py`

* Offers non-medical, generic suggestions based on fluency metrics

### 🔹 `requirements.txt`

* Basic deps: `whisper`, `torch`, `sounddevice`, `soundfile`, `cryptography`

---

## 🧪 How to Run

```bash
PYTHONPATH=. python scripts/record_and_analyze.py \
  --inputfile media_files/sample.wav \
  --action 2 --aeskey "..." --saveoutput out.txt
```

---

## ✅ Status

* Core system is working
* Ready for further extension
* Modular design (each tool swappable)
* CLI-first interface

This repo is structured to allow flexible experimentation with speech input, analysis, and post-processing.
# MADE BY GPT,O3-PRO,O3,O1-Pro
