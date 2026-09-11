# crypto/rsa_layer.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from typing import Tuple


def generate_rsa_keys(bits: int = 2048) -> Tuple[bytes, bytes]:
    key = RSA.generate(bits)
    private_key = key.export_key()      # bytes (PEM)
    public_key = key.publickey().export_key()
    return private_key, public_key

def rsa_wrap_key(aes_key: bytes, public_key_pem: bytes) -> bytes:
    """Encrypt (wrap) AES key with recipient's RSA public key PEM"""
    rsa_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(rsa_key)
    wrapped = cipher.encrypt(aes_key)
    return wrapped

def rsa_unwrap_key(wrapped_key: bytes, private_key_pem: bytes) -> bytes:
    """Decrypt wrapped AES key using RSA private key PEM"""
    rsa_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(rsa_key)
    aes_key = cipher.decrypt(wrapped_key)
    return aes_key
