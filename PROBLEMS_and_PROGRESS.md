# MADE BY CODEX,O3-PRO,O3,GPT
# 🧠 AI-SPEECH: Notes on Stuttering Support Attempts
This document captures what we've tried, what worked, and what didn't when attempting to build stuttering detection or support features using OpenAI Whisper.

---

## ✅ What We Built (And What Works Well)

### 🔹 1. Word Confidence Marker

* Uses Whisper's `word_timestamps=True` to extract per-word timestamps and approximate confidence.
* CLI tool: `scripts/word_confidence_marker.py`
* Marks each word as:

  * `word` if confident
  * `?word?` if uncertain
  * `??word??` if low-confidence
* Useful for **speech reflection**, not detection.

### 🔹 2. Confidence Threshold CLI

* User can control confidence brackets:

  ```bash
  --confident 0.92
  --unsure 0.55
  ```

### 🔹 3. Whisper Parameter Tweaks

* Added `--temp`, `--logprob`, and `--compression` to CLI
* Exposed Whisper internals for tuning output behavior
* Example: `--temp 0.8` lets Whisper be less confident and more raw

### 🔹 4. Batch Transcribe Script

* `scripts/batch_transcribe.py` sweeps through different Whisper settings
* Useful for testing how `temperature`, `logprob_threshold`, etc. affect output

### 🔹 5. Reflective, Non-Clinical Framing

* Focused on **awareness**, not diagnosis
* Avoided risky assumptions about stuttering detection

---

## ❌ What Didn't Work (And Why)

### ❌ Whisper Erases Disfluency By Design

* It smooths out “uhhh”, “I-I-I”, and stuttered fragments
* Even if you say "uhm" loudly, Whisper will usually drop it

### ❌ Whisper Does *Not* Return True Token-Level Confidence

* Whisper gives `avg_logprob` per segment, not per token
* Some forks (like [stable-ts](https://github.com/jianfch/stable-ts) or [SinanAkkoyun’s fork](https://github.com/SinanAkkoyun/openai-whisper/tree/token-confidence)) add token confidence
* But stock Whisper doesn’t support this

### ❌ Trying to Detect Stuttering from Transcript Alone

* We tried using repetitions + filler detection
* But since Whisper removes these, you can't reliably detect stuttering this way

### ❌ Confidence-based detection ≠ Stuttering detection

* Whisper’s word confidence is not always tied to speech difficulty
* Low confidence might just mean a soft-spoken word or noise

---

## ✅ What This Means Moving Forward

* Whisper is **great for clean transcript support**
* Whisper is **not ideal for raw disfluency detection**
* But we can use it as a tool for:

  * Reflecting on what was said
  * Visualizing fluency trends
  * Highlighting uncertain speech

# VITAL NOTE
We should avoid using Whisper to **claim** it detects stuttering. Instead, we can keep it as a reflective and exploratory speech support tool.

---

## Ideas for Future Exploration

* Use energy + silence detection directly from audio
* Manual tagging of known difficult segments
* **Let users mark "this felt hard to say" for feedback loops**
* *maybe different ways to say same thing*
* Integrate TTS replay: “This is how you said it” vs “This is a smoother version”
* If needed: Explore Whisper forks that include `token_probs[]`

---
