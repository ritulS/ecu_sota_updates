# Script to generate VVM 
# Will run on primary ECU
# Inputs: Hash of all secondary ecus and their respective Sym keys
# Output: to be sent to server
'''(dictionary format)
    vvm = {
        ecu1: {
        signed: { image_hash: "hash"},
        ecu_name: "",
        signature: "dafkljlj",
        nonce: nonce,
        tag: tag,
        cipher_text: cipher_text
        },
        ecu2: {
        signed: {image_hash: "hash"},
        signature: "dafkljlj"
        nonce: nonce,
        tag: tag,
        cipher_text: cipher_text
        }
        vin: "id-number"
    }
'''


# ed255196 for signature
# SHA-512/256 for hashing



class prim_ecu:
    id: str
    sym_key: str
    img_hash: str

    def request_ecu_man(self):
        pass

    def receive_ecu_man(self):
        pass

    def gen_vvm(self):
        pass


