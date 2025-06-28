# 🧪 AI-SPEECH TOOLKIT — EXAMPLES.MD
# Made By CODEX,O3-PRO and O3

This document shows **real CLI examples** of everything your AI-Speech system can do:
record, transcribe, encrypt, decrypt, analyze, keyword scan — and combine them.

---

##  RECORD AUDIO FROM MIC

```bash
PYTHONPATH=. python scripts/record_and_analyze.py \
  --duration 5 \
  --saveoutput record.json
```

* Records 5 seconds from your microphone
* Transcribes it
* Outputs transcript, analysis, and tips to `record.json`

---

## TRANSCRIBE EXISTING AUDIO FILE (MP3/WAV)

```bash
PYTHONPATH=. python scripts/record_and_analyze.py \
  --inputfile media_files/my_clip.mp3
```

* Reads the file
* Transcribes and analyzes
* Shows transcript, disfluency count, and fluency tips

---

## ENCRYPT TRANSCRIPTION WITH AES-256

```bash
PYTHONPATH=. python scripts/record_and_analyze.py \
  --inputfile media_files/my_clip.mp3 \
  --action 2 \
  --aeskey "YOUR_BASE64_AES_KEY" \
  --saveoutput encrypted.txt
```

* Action 2 = AES encrypt text (using your key)
* Output is a base64-encoded AES blob

---

## DECRYPT ENCRYPTED TEXT (ACTION 2 or 3)

```bash
PYTHONPATH=. python ai_speech/actions.py \
  --decrypt "<your AES-encoded string>" \
  --aeskey "YOUR_BASE64_AES_KEY"
```

* Decrypts and returns readable transcript
* Key must be base64 and decode to 16, 24, or 32 bytes

---

## KEYWORD SCAN FROM AUDIO

```bash
PYTHONPATH=. python scripts/record_and_analyze.py \
  --inputfile media_files/my_clip.mp3 \
  --action 4
```

* Detects keywords from built-in list + `ai_speech/keywords.txt`
* Action 4 prints matched terms (e.g. `lithium, uranium, yellow gas`)

---

## REVERSE-ENCRYPT SPEECH (ENCRYPT THEN REVERSE)

```bash
PYTHONPATH=. python scripts/record_and_analyze.py \
  --inputfile media_files/my_clip.mp3 \
  --action 3 \
  --aeskey "YOUR_BASE64_AES_KEY"
```

* Same as action 2 but with result reversed
* Useful for obfuscation + encoding

---

## 📑 RUN ACTIONS ON TEXT (WITHOUT AUDIO)

```bash
PYTHONPATH=. python ai_speech/actions.py \
  --mode 4 \
  "this test discusses uranium, chlorine and fire"
```

* Processes directly via CLI
* No audio needed

---

## SAMPLE `keywords.txt` (optional, auto-loaded)

Located at: `ai_speech/keywords.txt`

```text
agent orange
CL2
yellow mist
trigger device
industrial peroxide
```

Used by `--action 4` to detect additional sensitive terms

---

## VERIFY SETUP

```bash
openssl rand -base64 32  # Generate strong AES key
```

```bash
PYTHONPATH=. python ai_speech/actions.py \
  --text "fire bomb chemical" \
  --mode 2 \
  --aeskey "<base64 key>"
```

Then:

```bash
PYTHONPATH=. python ai_speech/actions.py \
  --decrypt "<output from above>" \
  --aeskey "<base64 key>"
```

---

### comments from the prompter LoneIceWolf
- I didn't expect this project to be so all including, including cryptography, keywords scanning, and so on and so forth, it became a much Much bigger project than I've imagined it to be!
