import can
import sys

from ip_link import Ip_link

can.rc['interface'] = "socketcan"
can.rc['channel'] = "can0"
can.rc['bitrate'] = 500000

def recv_msg():
    with Ip_link() as ip_link:
        with can.Bus() as bus:
            try:
                print("LISTENING")
                while True:
                    msg = bus.recv()

                    id = f"[{msg.timestamp}] {msg.arbitration_id} {msg.dlc}"

                    data = ''
                    for i in range(msg.dlc):
                        data += f"{msg.data[i]}"

                    print(f"{id}: {data}")
                    continue

            except KeyboardInterrupt:
                print("KEYBOARD INTERRUPT")


if __name__ == "__main__":
    recv_msg()

