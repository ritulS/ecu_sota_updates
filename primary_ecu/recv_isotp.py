import sys
import time
import logging
import threading
import json

import can
import isotp

from ip_link import Ip_link


can.rc['interface'] = "socketcan"
can.rc['channel'] = "can0"
can.rc['bitrate'] = 500000

# CANID: 0x789
class ThreadedListen:
    def __init__(self, rxid = None, txid = None):
        print("From threaded", rxid, txid)
        # self.get_can_id()
        self.id = rxid if rxid else self.get_can_id()
        self.txid = txid if txid else 0x123
        self.exit_requested = False
        self.bus = can.Bus()
        addr = isotp.Address(
                isotp.AddressingMode.Normal_11bits,
                rxid=self.id,
                txid=self.txid,
            )
        self.stack = isotp.CanStack(
                self.bus,
                address=addr,
                error_handler=self.error_handler,
                params={
                    "max_frame_size": 2097152
                }
            )
    def get_can_id(self) -> int:
        with open("/home/pi/ecu_info.json") as _file:
            f = _file.read()
            info = json.loads(f)

            # print(int(info['can_id'], 16))
            return int(info['can_id'], 16)

    def start(self):
        self.exit_requested = False
        self.thread = threading.Thread(target = self.thread_task)
        self.thread.start()

    def thread_task(self):
        while self.exit_requested == False:
            self.stack.process()
            time.sleep(self.stack.sleep_time())

    def stop(self):
        self.exit_requested = True
        if self.thread.is_alive():
            self.thread.join()

    def error_handler(self, error):
        logging.warning("IsoTp error happened: %s - %s" % (error.__class__.__name__, str(error)))

    def shutdown(self):
        self.stop()
        self.bus.shutdown()

def error_handler(error):
    logging.warning("IsoTp error: %s - %s" % (error.__class__.__name__, str(error)))

def send_manifest():
    with can.Bus() as bus:
        addr = isotp.Address(
                isotp.AddressingMode.Normal_11bits,
                txid=0x123,
                rxid=0x789
        )
        stack = isotp.CanStack(
                bus,
                address = addr,
                error_handler=error_handler
        )

        stack.send(b'jsonfile')

        with stack.transmitting():
            stack.process()
            time.sleep(stack.sleep_time())

def listen_for_data(data, callbackFn = None, txid = None, rxid = None):
    with Ip_link() as ip_link:
        app = ThreadedListen(txid = txid, rxid = rxid)
        app.start()

        try:
            print("LISTENING...")

            while True:
                if app.stack.available():
                    print("avail")
                    payload = app.stack.recv()
                    print("Received payload: %s" % (payload))

                    if payload == data:
                        break

                time.sleep(0.2)

            print("EXITING")
            app.shutdown()

            if callbackFn:
                callbackFn()

        except KeyboardInterrupt:
            print("KI, exiting")
            app.shutdown()

        if callbackFn:
            callbackFn()

def listen_everything():
    with Ip_link() as ip_link:
        app = ThreadedListen()
        app.start()

        try:
            print("LISTENING")

            while True:
                if app.stack.available():
                    payload = app.stack.recv()
                    print("Received payload: %s" % (payload))
                    # print(payload.decode("utf-8"))

                    continue
                time.sleep(0.2)

            print("EXITING")
            app.shutdown()
        except KeyboardInterrupt:
            print("KI, exiting")
            app.shutdown()


if __name__ == "__main__":
    listen_for_data(b'send data bitches', send_manifest)

