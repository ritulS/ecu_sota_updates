from typing import Any
from primary_ecu.ecu_man import ecu_input
from Crypto.Cipher import AES
from Crypto.Cipher._mode_eax import EaxMode

def main():
    key = bytes.fromhex('6580f3956d19dcfa397ce84767f84a32')
    inp = ecu_input("./file.bin")
    manifest = inp.gen_ecu_manifest()

    cipher: Any = AES.new(key, AES.MODE_EAX, nonce=manifest.nonce)

    if isinstance(cipher, EaxMode):
        cipher.decrypt_and_verify(manifest.cipher_text, received_mac_tag=manifest.tag)

if __name__ == "__main__":
    main()
