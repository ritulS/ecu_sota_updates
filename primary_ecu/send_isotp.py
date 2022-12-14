import sys
import logging
import time
import json
import os

import isotp
import can

from ip_link import Ip_link

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 500000

def error_handler(error):
    logging.warning("IsoTp error: %s - %s" % (error.__class__.__name__, str(error)))

def send_msg(txid = 0x123, rxid = 0x456):
    with Ip_link() as ip_link:
        with can.Bus() as bus:
            addr = isotp.Address(
                    isotp.AddressingMode.Normal_11bits,
                    rxid=rxid,
                    txid=txid,
                )

            _data = b"jsonfile"

            stack = isotp.CanStack(
                    bus,
                    address=addr,
                    error_handler=error_handler,
                    params={
                        "max_frame_size": 2097152
                    }
                )
            stack.send(_data)

            while stack.transmitting():
                stack.process()
                time.sleep(stack.sleep_time())

def main():
    send_msg()

if __name__ == "__main__":
    main()
