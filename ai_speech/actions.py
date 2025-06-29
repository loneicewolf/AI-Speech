"""
Actions Processing Module
=========================
Post‑transcription utilities that can be chained onto Whisper output.
The module can be imported **or** run as a CLI helper for unit testing.

New in v1.1  (2025‑06‑28)
------------------------
* Keyword list is now **file‑driven** – drop a plain‑text file (one keyword per line)
  and the search will automatically extend.
* Added **AES‑CBC** encryption helper (falls back to base64 if `cryptography` is
  missing) so you can swap in any crypto function you like.
* Added a **JSON save** utility so the parent CLI can dump results to disk when
  `--saveoutput result.json` is passed.
* Added **AES decryption** utility to decode `action_2` or `action_3` outputs.
"""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import List, Dict, Optional

#######################################################################
# GENERIC HELPERS
#######################################################################

DEFAULT_KEYWORD_FILE = Path(__file__).with_name("keywords.txt")

#######################################################################
# ACTION 1 – RAW TEXT                                                  #
#######################################################################

def action_1_text_only(text: str) -> str:
    """Return the raw transcribed text unchanged."""
    return text

#######################################################################
# ACTION 2 – ENCRYPT TEXT (BASE64 OR AES)                              #
#######################################################################

def _aes_encrypt(text: str, key: bytes) -> str:
    """Encrypt text with AES‑CBC (fallback if cryptography is present)."""
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.backends import default_backend
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        padder = padding.PKCS7(128).padder()
        padded = padder.update(text.encode()) + padder.finalize()
        enc = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
        return base64.b64encode(iv + enc).decode()
    except Exception as e:
        return f"[AES encryption failed] {str(e)}"


def _aes_decrypt(encoded: str, key: bytes) -> str:
    """Decrypt AES-CBC base64 string."""
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.backends import default_backend
        data = base64.b64decode(encoded)
        iv, ciphertext = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decrypted = cipher.decryptor().update(ciphertext) + cipher.decryptor().finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return (unpadder.update(decrypted) + unpadder.finalize()).decode()
    except Exception as e:
        return f"[Decryption failed] {str(e)}"


def action_2_encrypt_text(text: str, *, key: bytes | None = None) -> str:
    """Encrypt the text (AES‑CBC if key provided, else base64)."""
    if key:
        return _aes_encrypt(text, key)
    return base64.b64encode(text.encode()).decode()


def action_decrypt(encrypted_text: str, key: bytes) -> str:
    """Manually decrypt a message (AES-CBC with base64)."""
    return _aes_decrypt(encrypted_text, key)

#######################################################################
# ACTION 3 – ENCRYPT + REVERSE                                         #
#######################################################################

def action_3_encrypt_and_reverse(text: str, *, key: bytes | None = None) -> str:
    enc = action_2_encrypt_text(text, key=key)
    return enc[::-1]

#######################################################################
# ACTION 4 – KEYWORD SCAN                                              #
#######################################################################

def _load_keywords(extra: Optional[List[str]] = None) -> List[str]:
    kws: List[str] = [
        "password", "bomb", "uranium", "hexafluoride", "root", "admin", "agent",
        "lithium", "soft metal", "chlorine", "yellow gas", "fire", "heat", "chemical",
    ]
    if DEFAULT_KEYWORD_FILE.exists():
        kws.extend(k.strip() for k in DEFAULT_KEYWORD_FILE.read_text().splitlines() if k.strip())
    if extra:
        kws.extend(extra)
    return list(dict.fromkeys(kws))


def action_4_keyword_search(text: str, *, extra: Optional[List[str]] = None) -> List[str]:
    keywords = _load_keywords(extra)
    return [kw for kw in keywords if kw.lower() in text.lower()]

#######################################################################
# PUBLIC API                                                          #
#######################################################################

action_map = {
    1: action_1_text_only,
    2: action_2_encrypt_text,
    3: action_3_encrypt_and_reverse,
    4: action_4_keyword_search,
}


def run_action_mode(transcript: Dict[str, str], mode: int = 1, **kwargs) -> str:
    """Run a specific post‑processing action and return its result."""
    text = transcript.get("text", "")
    func = action_map.get(mode)
    if func is None:
        return "Invalid action mode."
    result = func(text, **kwargs)
    if isinstance(result, list):
        return ", ".join(result)
    return str(result)


def run_all_actions(transcript: Dict[str, str]) -> Dict[str, str]:
    """Run *all* actions and return dictionary of results."""
    return {f.__name__: f(transcript.get("text", "")) for f in action_map.values()}

#######################################################################
# CLI TEST HOOK                                                       #
#######################################################################

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Quick‑test the action pipeline")
    parser.add_argument("text", nargs="*", help="Sample text to process")
    parser.add_argument("--mode", type=int, choices=range(1, 5), default=1)
    parser.add_argument("--aeskey", type=str, help="Optional AES key (16/24/32 bytes)")
    parser.add_argument("--decrypt", type=str, help="Decrypt given base64 string")
    parser.add_argument("--saveoutput", type=Path, help="Optional path to save JSON output")
    args = parser.parse_args()

    if args.decrypt and args.aeskey:
        try:
            key = base64.b64decode(args.aeskey)
        except Exception as e:
            raise ValueError(f"Invalid base64 key: {e}")
        print(action_decrypt(args.decrypt, key))
        exit()

    sample_transcript = {"text": " ".join(args.text) or "This is a lithium battery fire talking about yellow gas."}
    kwargs = {}
    if args.aeskey:
        try:
            key = base64.b64decode(args.aeskey)
            if len(key) not in (16, 24, 32):
                raise ValueError
        except Exception:
            raise ValueError("AES key must be base64-encoded and decode to 16, 24, or 32 bytes")
        kwargs["key"] = key

    output = run_action_mode(sample_transcript, mode=args.mode, **kwargs)

    if args.saveoutput:
        args.saveoutput.write_text(json.dumps({"result": output}, indent=2, ensure_ascii=False))
        print(f"✅ Saved to {args.saveoutput}")
    else:
        print(output)
