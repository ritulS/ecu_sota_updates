import sys
import logging
import time

import isotp
import can

from ip_link import Ip_link
from misc import setup_config, parse_args, get_file_contents

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 500000

def error_handler(error):
    logging.warning("IsoTp error: %s - %s" % (error.__class__.__name__, str(error)))

def send_msg(iD = 0x123, data = [1, 2, 3 ,4 , 5 ,5 ,6, 7]):
    with Ip_link() as ip_link:
        with can.Bus() as bus:
            addr = isotp.Address(
                    isotp.AddressingMode.Normal_11bits,
                    rxid=0x123,
                    txid=0x456,
                )

            _data = get_file_contents("file.bin")

            stack = isotp.CanStack(
                    bus,
                    address=addr,
                    error_handler=error_handler,
                    params={
                        "max_frame_size": 2097152
                    }
                )
            # stack.send(b'this is a realllllly lllllooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong payload')
            stack.send(_data)

            while stack.transmitting():
                stack.process()
                time.sleep(stack.sleep_time())

if __name__ == "__main__":
    send_msg()