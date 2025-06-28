"""Utility actions for processing transcripts and text."""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path
from typing import Iterable

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# Load keyword list (one term per line)
KEYWORDS: set[str] = set()
keywords_file = Path(__file__).with_name("keywords.txt")
if keywords_file.exists():
    with keywords_file.open("r", encoding="utf-8") as f:
        KEYWORDS.update(line.strip().lower() for line in f if line.strip())


# -- AES utilities -----------------------------------------------------------

def _aes_cipher(key: bytes, iv: bytes) -> Cipher:
    return Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())


def aes_encrypt(text: str, key: bytes) -> str:
    """Encrypt text with AES-CBC and return base64 string."""
    iv = os.urandom(16)
    cipher = _aes_cipher(key, iv)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded = padder.update(text.encode("utf-8")) + padder.finalize()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode("utf-8")


def aes_decrypt(data_b64: str, key: bytes) -> str:
    """Decrypt base64 AES-CBC data and return plaintext."""
    raw = base64.b64decode(data_b64)
    iv, ciphertext = raw[:16], raw[16:]
    cipher = _aes_cipher(key, iv)
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded) + unpadder.finalize()
    return data.decode("utf-8")


# -- Action modes -----------------------------------------------------------

def run_action_mode(transcript: dict | str, *, mode: int, key: bytes | None = None) -> str:
    """Run a post-processing action on a transcript or plain text."""
    if isinstance(transcript, dict):
        text = transcript.get("text", "")
    else:
        text = str(transcript)

    if mode == 1:
        return text

    if mode in (2, 3):
        if not key:
            raise ValueError("AES key required for modes 2 and 3")
        if mode == 3:
            text = text[::-1]
        return aes_encrypt(text, key)

    if mode == 4:
        words = set(text.lower().split())
        matches = sorted(w for w in KEYWORDS if any(w in word for word in words))
        return ", ".join(matches)

    raise ValueError(f"Unsupported mode: {mode}")


# -- CLI -------------------------------------------------------------------

def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run AI-Speech actions")
    parser.add_argument("--mode", type=int, choices=range(1, 5), help="Action mode")
    parser.add_argument("--aeskey", help="Base64-encoded AES key")
    parser.add_argument("--decrypt", help="Base64 text to decrypt")
    parser.add_argument("--text", help="Plain text input (for modes without audio)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    key = base64.b64decode(args.aeskey) if args.aeskey else None

    if args.decrypt:
        if not key:
            raise SystemExit("--aeskey required for --decrypt")
        print(aes_decrypt(args.decrypt, key))
        return

    if not args.text:
        raise SystemExit("--text is required when not decrypting")
    result = run_action_mode(args.text, mode=args.mode, key=key)
    print(result)


if __name__ == "__main__":
    main()
