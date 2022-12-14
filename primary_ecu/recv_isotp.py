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
    def __init__(self, rxid, txid):
        print("From threaded", rxid, txid)
        self.id = rxid
        self.txid = txid
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
                error_handler=error_handler,
                params={
                    "max_frame_size": 2097152
                }
            )
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

    def shutdown(self):
        self.stop()
        self.bus.shutdown()

def error_handler(error):
    logging.warning("IsoTp error: %s - %s" % (error.__class__.__name__, str(error)))

def listen_for_data(data, txid, rxid, callbackFn = None):
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
            time.sleep(5)

            if callbackFn:
                callbackFn()

        except KeyboardInterrupt:
            print("KI, exiting")
            app.shutdown()

def listen_for_data_ecu(listen_for, txid, rxid):
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

                    if payload == listen_for:
                        break

                time.sleep(0.2)

            print("EXITING")
            app.shutdown()

            return True

        except KeyboardInterrupt:
            print("KI, exiting")
            app.shutdown()
            return False

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

