import can
import sys

from ip_link import Ip_link

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 500000

def send_msg(iD, data):
    with Ip_link() as ip_link:
        with can.Bus() as bus:
            msg = can.Message(
                arbitration_id=0x1111, data=[11, 12, 13, 14, 15, 16, 17, 18]
            )

            try:
                bus.send(msg)
                print(f"Message Sent on channel: {bus.channel_info}")
            except can.CanError:
                print("ERROR OCCURED", can.CanError)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        print("[ID#MSG]")
        _msg = sys.argv[1].strip().split("#")

        iD = _msg[0]
        data = _msg[1]

        send_msg(iD, data)
