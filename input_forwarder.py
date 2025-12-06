import struct

INPUT_DEVICE = "/dev/input/event0"  # Adjust if needed
UDP_IP = "127.0.0.1"
UDP_PORT = 4444

# Event format: struct input_event { struct timeval time; __u16 type; __u16 code; __s32 value; };
EVENT_FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

def send_udp(message):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (UDP_IP, UDP_PORT))

def main():
    try:
        f = open(INPUT_DEVICE, "rb")
        while True:
            data = f.read(EVENT_SIZE)
            if data:
                (tv_sec, tv_usec, type, code, value) = struct.unpack(EVENT_FORMAT, data)
                if type == 1 and value == 1: # EV_KEY, Pressed
                    print("Key pressed: code=%d" % code)
                    # Send to info-beamer via UDP
                    # Expected by util.data_mapper: "path/to/listener:payload"
                    send_udp("input:%d" % code)
    except Exception as e:
        print(e)
        import time
        time.sleep(5)

if __name__ == "__main__":
    main()
