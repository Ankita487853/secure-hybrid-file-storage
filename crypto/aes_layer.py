from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def pad(data):
    """PKCS7 padding"""
    padding_len = 16 - (len(data) % 16)
    return data + bytes([padding_len]) * padding_len

def unpad(data):
    """Remove PKCS7 padding"""
    padding_len = data[-1]
    return data[:-padding_len]

def aes_encrypt(data):
    key = get_random_bytes(32)  # AES-256 key
    iv = get_random_bytes(16)   # Initialization vector

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data))

    return encrypted_data, key, iv

def aes_decrypt(enc_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(enc_data))
    return decrypted
