import sys


def setup_config():
    can.rc['interface'] = 'socketcan'
    can.rc['channel'] = 'can0'
    can.rc['bitrate'] = 500000


def parse_args(args: list[str]):
    _msg = sys.argv[1].strip().split("#")

    iD = _msg[0]
    data = _msg[1]

    if 'x' in iD:
        iD = int(iD, 16)
    else:
        iD = int(iD)

    if iD > (2**29 - 1):
        print("CAN ID exceeds 2^11 - 1")
        sys.exit(1)

    if 'b' in data:
        data = bytes(data[2:-1], "utf-8")
    else:
        data = list(map(int, data.strip().split(",")))

    if len(data) > 8:
        print("Frame length can't be more than 8")

    print(iD, data)

    return iD, data

def get_file_contents(file_name: str):
    with open(file_name, 'rb') as f:
        return f.read()

