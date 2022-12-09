# Script to generate VVM 
# Will run on primary ECU
# Inputs: Hash of all secondary ecus and their respective Sym keys
# Output: Concatenation of Signed hashes of all secondary ecus


# ed255196 for signature
# SHA-512/256 for hashing



class prim_ecu:
    id: str
    sym_key: str
    img_hash: str


    def req_ecu_man(self):
        pass

    def receive_ecu_man(self):
        pass
    
    def gen_vvm(self):
        pass

'''
# {
#   ecu1: {
#   signed: { image_hash: "hash"},
#   ecu_name: "",
#   signature: "dafkljlj"
#   },
#   ecu2: {
#   signed: {image_hash: "hash"},
#   signature: "dafkljlj"
#   }
#   vin: "id-number"
# }
'''