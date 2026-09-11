# crypto/chaotic_key.py
import hashlib
import struct
from typing import Tuple

def _float_to_bytes(x: float) -> bytes:
    """Deterministic conversion of float -> 32 bytes via SHA256 of repr"""
    return hashlib.sha256(repr(x).encode()).digest()

def chaotic_mask_from_seed(seed: float, length: int, r: float = 3.99, burn: int = 100) -> bytes:
    """
    Produce `length` bytes of mask from logistic map with parameter r and seed.
    burn: number of initial iterations to skip to avoid transient behavior.
    """
    x = float(seed)
    mask = b''
    # burn-in
    for _ in range(burn):
        x = r * x * (1 - x)
    while len(mask) < length:
        x = r * x * (1 - x)
        mask += _float_to_bytes(x)
    return mask[:length]

def mix_aes_key(aes_key: bytes, seed: float = None, r: float = 3.99, burn: int = 100) -> Tuple[bytes, dict]:
    """
    Mix the provided AES key with chaotic mask.
    Returns (mixed_key, meta) where meta contains seed/r/burn info required to reconstruct mask.
    If seed is None, caller should provide a seed (e.g., derived from os.urandom -> float).
    """
    if seed is None:
        raise ValueError("seed must be provided (float in (0,1))")
    mask = chaotic_mask_from_seed(seed, len(aes_key), r=r, burn=burn)
    mixed = bytes(a ^ b for a, b in zip(aes_key, mask))
    meta = {"seed": seed, "r": r, "burn": burn}
    return mixed, meta

def unmix_aes_key(mixed_key: bytes, meta: dict) -> bytes:
    """Recover original AES key using meta produced by mix_aes_key"""
    seed = float(meta["seed"])
    r = float(meta.get("r", 3.99))
    burn = int(meta.get("burn", 100))
    mask = chaotic_mask_from_seed(seed, len(mixed_key), r=r, burn=burn)
    orig = bytes(a ^ b for a, b in zip(mixed_key, mask))
    return orig
