"""
    utils.py

    Utilities to encrypt or decrypt the payload for Axis Direct REST APIs.

    :copyright: (c) 2024 Abhay Braja.
    :license: see LICENSE for details.
"""


import base64
import hashlib
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


def encrypt_aes(payload: str, secret_key: str):
    # convert the hex string secret key to bytes
    secret_key_bytes = secret_key.encode()
    # create an AES cipher object with GCM mode
    cipher = AES.new(secret_key_bytes, AES.MODE_GCM)
    # encrypt the payload
    ciphertext, tag = cipher.encrypt_and_digest(payload.encode())
    # encode the nonce, ciphertext, and tag as base64
    encoded_nonce = base64.b64encode(cipher.nonce).decode()
    encoded_tag = base64.b64encode(tag).decode()
    encoded_ciphertext = base64.b64encode(ciphertext).decode()
    # return the encoded payload
    return f"{encoded_nonce}.{encoded_tag}.{encoded_ciphertext}"


def encrypt_rsa(secret_key: str, public_key: str):
    # Converts a public key to PEM format.
    pem_string = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    # load the public key
    key = RSA.import_key(pem_string)
    # create an RSA OAEP cipher object
    cipher = PKCS1_OAEP.new(key, hashlib.sha256)
    # encrypt the payload
    encrypted_payload = cipher.encrypt(secret_key.encode())
    # encode the encrypted payload as base64
    encoded_payload = base64.b64encode(encrypted_payload).decode()
    return encoded_payload


def decrypt_data(encoded_payload: str, secret_key: str):
    # convert the hex string secret key to bytes
    secret_key_bytes = secret_key.encode()
    # split the encoded payload into the nonce, ciphertext, and tag
    encoded_nonce, encoded_tag, encoded_ciphertext = encoded_payload.split(".")
    # decode the nonce, ciphertext, and tag from base64
    nonce = base64.b64decode(encoded_nonce)
    tag = base64.b64decode(encoded_tag)
    ciphertext = base64.b64decode(encoded_ciphertext)
    # create an AES cipher object with GCM mode
    cipher = AES.new(secret_key_bytes, AES.MODE_GCM, nonce=nonce)
    # decrypt the payload
    decrypted_payload = cipher.decrypt_and_verify(ciphertext, tag).decode()
    return decrypted_payload
