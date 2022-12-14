import time
import subprocess

from recv_isotp import listen_for_data_ecu

def main():
    got_the_msg = listen_for_data_ecu(
        listen_for = b'send_ecu_data',
        rxid = 0x456,
        txid = 0x123,
    )
    time.sleep(1)

    subprocess.run(["python", "/home/pi/ecu_sota_updates/primary_ecu/send_isotp.py"])

if __name__ == "__main__":
    main()
