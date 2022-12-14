import sys
import logging
import time
import json
import os

import isotp
import can

from ip_link import Ip_link
from ecu_man import ecu_input

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 500000

def get_ecuinfo():
    with open("/home/pi/ecu_info.json", "r") as _f:
        _file = _f.read()
        info = json.loads(_file)

        return info

def error_handler(error):
    logging.warning("IsoTp error: %s - %s" % (error.__class__.__name__, str(error)))

def send_msg(txid = 0x123, rxid = 0x456):
    print("[ECU] RECEIVED MANIFEST REQUEST")
    
    _data = ecu_input("/home/pi/ecu_info.json").gen_ecu_manifest()
    ecu_info = get_ecuinfo()
    json_data = {
        ecu_info['ecu_name']: {
            'cipher_text': str(_data.cipher_text),
            'tag': str(_data.tag),
            'nonce': str(_data.nonce),
            'sr_num': str(_data.sr_num),
        }
    }
    json_data = b'|' + _data.cipher_text + b'|' + _data.tag + b'|' + _data.nonce + b'|' + _data.sr_num.encode('utf-8')

    with Ip_link() as ip_link:
        with can.Bus() as bus:
            addr = isotp.Address(
                    isotp.AddressingMode.Normal_11bits,
                    rxid=rxid,
                    txid=txid,
                )

            data = b'jsonfile' + json_data

            stack = isotp.CanStack(
                    bus,
                    address=addr,
                    error_handler=error_handler,
                    params={
                        "max_frame_size": 2097152
                    }
                )
            stack.send(data)

            while stack.transmitting():
                stack.process()
                time.sleep(stack.sleep_time())
        print("[ECU] SENT MAINFEST DATA TO PRIMARY")

def main():
    send_msg()

if __name__ == "__main__":
    main()
