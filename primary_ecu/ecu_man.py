# Install Py cryptodom
# Generates ECU manifest
# Input: symmetric key of ECU, image 

# AES for symmetric signature
# SHA-512/256 for hashing

from dataclasses import dataclass
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from Crypto.Cipher._mode_eax import EaxMode
from typing import Any, Tuple

@dataclass
class ecu_manifest:
    cipher_text: bytes
    tag: bytes
    nonce: bytes
    sr_num: str

class ecu_input:
    def __init__(self, file_name: str) -> None:
        self.file_name =  file_name

    def _load_file(self) -> bytes:
        with open(self.file_name, "rb") as file:
            return file.read()

    def _hash_and_sign(self) -> Tuple[ bytes, bytes, bytes ]:
        img_byte_str = self._load_file()

        key = bytes.fromhex('6580f3956d19dcfa397ce84767f84a32')
        hash = SHA512.new()
        hash.update(img_byte_str)
        img_hash = hash.digest()


        cipher: Any = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce

        if isinstance(cipher, EaxMode):
            cipher_text, tag = cipher.encrypt_and_digest(img_hash)

            return cipher_text, tag, nonce
        else:
            raise Exception("---- TypeMismatch ----")


    def gen_ecu_manifest(self) -> ecu_manifest:
        cipher_text, tag, nonce = self._hash_and_sign()

        return  ecu_manifest(
            cipher_text= cipher_text,
            sr_num = "harcoded",
            nonce = nonce,
            tag = tag
        )
        # return manifest
