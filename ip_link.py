import subprocess
import time
import sys

class Ip_link(object):
    def __init__(self):
        pass

    def __enter__(self):
        print(" --- Setting can0 --- ")

        try:
            subprocess.run(
                ["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate", "500000"],
                check = True
            )
        except subprocess.CalledProcessError:
            print("{ERROR} [CAN'T SET UP IP LINK]")
            sys.exit(1)

        print(" --- Done setting up can0 --- \n\n")
        time.sleep(0.1)

    def __exit__(self, *args):
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

