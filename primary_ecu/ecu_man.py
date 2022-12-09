# Install Py cryptodom
# Generates ECU manifest
# Input: symmetric key of ECU, image 

# AES for symmetric signature
# SHA-512/256 for hashing

from dataclasses import dataclass
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
# from Crypto.Cipher._mode_eax import EaxMode
from typing import Any, Tuple

@dataclass
class ecu_manifest:
    cipher_text: bytes
    tag: bytes
    sr_num: str

class ecu_input:
    id: str
    sym_key: str
    img_byte_str: str

    def __init__(self, file_name: str) -> None:
        self.file_name =  file_name
        pass

    def _load_file(self, file_name: str) -> bytes:
        with open(file_name, "rb") as file:
            return file.read()

    def _hash_and_sign(self) -> Tuple[ bytes, bytes ]:
        img_byte_str = self._load_file("./file.bin")
        key = b'ecuKey' #Use the hardcoded key here
        hash = SHA512.new()
        hash.update(img_byte_str)
        img_hash = hash.digest()


        cipher: Any = AES.new(key, AES.MODE_EAX)
        # if isinstance(cipher, EaxMode):
        cipher_text, tag = cipher.encrypt_and_digest(img_hash)

        return cipher_text, tag 


    def gen_ecu_manifest(self) -> ecu_manifest:
        cipher_text, tag = self._hash_and_sign()

        return  ecu_manifest(
            cipher_text= cipher_text,
            sr_num = "harcoded",
            tag = tag
        )
        # return manifest
