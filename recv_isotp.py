import sys
import time
import logging
import threading

import can
import isotp

from ip_link import Ip_link


can.rc['interface'] = "socketcan"
can.rc['channel'] = "can0"
can.rc['bitrate'] = 500000

class ThreadedApp:
    def __init__(self):
        self.exit_requested = False
        self.bus = can.Bus()
        addr = isotp.Address(isotp.AddressingMode.Normal_11bits, rxid=0x456, txid=0x123)
        self.stack = isotp.CanStack(self.bus, address=addr, error_handler=self.error_handler)

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


if __name__ == "__main__":
    with Ip_link() as ip_link:
        app = ThreadedApp()
        app.start()
        try:
            print("LISTENING")
            # t1 = time.time()
            while True:
                if app.stack.available():
                    payload = app.stack.recv()
                    print("Received payload: %s" % (payload))
                    continue
                time.sleep(0.2)

            print("EXITING")
            app.shutdown()
        except KeyboardInterrupt:
            print("KI, exiting")
            app.shutdown()
