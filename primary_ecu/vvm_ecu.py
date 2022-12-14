import sys
import time
import logging
import threading
import json

import can
import isotp

from ip_link import Ip_link
from recv_isotp import ThreadedListen
from recv_isotp import listen_everything, listen_for_data


def send_manifest():
    print("[ECU] RECEIVED MANIFEST REQUEST")
    with can.Bus() as bus:
        addr = isotp.Address(
                isotp.AddressingMode.Normal_11bits,
                txid=0x456,
                rxid=0x123
        )
        stack = isotp.CanStack(
                bus,
                address = addr,
                error_handler=error_handler
        )

        stack.send(b'jsonfile')

        if stack.transmitting():
            stack.process()
            time.sleep(stack.sleep_time())
    print("[ECU] SENT MAINFEST DATA TO PRIMARY")

if __name__ == "__main__":
    listen_for_data(b'send_ecu_data', send_manifest)
