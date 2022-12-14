import sys
import time
import logging
import threading
import json
import subprocess

import can
import isotp

from ip_link import Ip_link
from recv_isotp import ThreadedListen
from recv_isotp import listen_everything, listen_for_data, listen_for_data_ecu


def error_handler(error):
    logging.warning("IsoTp error: %s - %s" % (error.__class__.__name__, str(error)))

def send_manifest():
    print("[ECU] RECEIVED MANIFEST REQUEST")
    with Ip_link() as ip_link:
        with can.Bus() as bus:
            addr = isotp.Address(
                    isotp.AddressingMode.Normal_11bits,
                    txid=0x123,
                    rxid=0x456
            )
            data = b'jsonfile'
            stack = isotp.CanStack(
                    bus,
                    address = addr,
                    error_handler=error_handler,
                    params={
                        "max_frame_size": 2097152
                    }
            )

            stack.send(data)

            if stack.transmitting():
                stack.process()
                print(stack.sleep_time())
                time.sleep(stack.sleep_time())

        print("[ECU] SENT MAINFEST DATA TO PRIMARY")

if __name__ == "__main__":
    got_the_msg = listen_for_data_ecu(
        listen_for = b'send_ecu_data',
        rxid = 0x456,
        txid = 0x123,
    )
    time.sleep(1)

    subprocess.run(["python", "/home/pi/ecu_sota_updates/primary_ecu/send_isotp.py"])

