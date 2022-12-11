# from pi_can.send_isotp import send_msg
# Script to generate VVM 
# Will run on primary ECU
# Inputs: Hash of all secondary ecus and their respective Sym keys
# Output: to be sent to server

# ed255196 for signature
# SHA-512/256 for hashing

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

import time
import subprocess
import threading
import sys
import logging

import can
import isotp

from recv_isotp import ThreadedListen

can.rc['interface'] = "socketcan"
can.rc['channel'] = "can0"
can.rc['bitrate'] = 500000

class PrimaryECU:
    def __init__(self):
        self.id = '123'
        self.can_id = 0x123
        self.ecu_info = [
            {
                "ecu_name": "ecu1_abscm",
                "can_id": 0x456
            },
            {
                "ecu_name": "ecu2_srscm",
                "can_id": 0x789
            },
        ]

    def get_params(self):
        pass

    def error_handler(self, error):
        logging.warning("IsoTp error: %s - %s" % (error.__class__.__name__, str(error)))

    def send_data(self, txid, data):
        with can.Bus() as bus:
            addr = isotp.Address(
                    isotp.AddressingMode.Normal_11bits,
                    txid=0x789,
                    rxid=self.can_id
            )
            stack = isotp.CanStack(
                    bus,
                    address = addr,
                    error_handler=self.error_handler
            )
            stack.send(data)

            while stack.transmitting():
                stack.process()
                time.sleep(stack.sleep_time())

    def request_ecu_man(self):
        for ecu in self.ecu_info:
            print(ecu['can_id'])
            self.send_data(ecu["can_id"], data=b'send data bitches')

    def receive_ecu_man(self):
        pass

    def gen_vvm(self):
        pass

    def start(self):
        print(" --- Setting can0 --- ")

        try:
            proc = subprocess.run(
                ["sudo", "ip", "link", "show", "can0", "up"],
                check = True,
                capture_output = True
            )

            if proc.stdout:
                print(" --- CAN Bus Already Setup --- \n\n")
            else:
                subprocess.run(
                    ["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate", "500000"],
                    check = True
                )

                print(" --- Done setting up can0 --- \n\n")
        except subprocess.CalledProcessError:
            print("{ERROR} [CAN'T SET UP IP LINK]")
            sys.exit(1)

        time.sleep(0.1)

    def stop(self):
        print("\n\n --- Closing can0 --- ")

        try:
            subprocess.run(
                ["sudo", "ip", "link", "set", "can0", "down"],
                check = True
            )
        except subprocess.CalledProcessError:
            print("{ERROR} [CAN'T SET UP IP LINK]")
            sys.exit(1)
        print(" --- Done setting can0 down --- \n\n")
        time.sleep(0.1)


if __name__ == "__main__":
    app = PrimaryECU()

    app.start()
    app.request_ecu_man()


    app.stop()
