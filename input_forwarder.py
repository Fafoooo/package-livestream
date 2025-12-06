import struct
import socket
import sys
import time

INPUT_DEVICE = "/dev/input/event1"
EVENT_FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

def send_udp(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Try sending to localhost and LAN, with and without newline
        # to catch whatever the parser prefers.
        targets = [("127.0.0.1", 4444), ("192.168.1.54", 4444)]
        
        # Send raw
        for t in targets:
            sock.sendto(message, t)
            
        # Send with newline
        for t in targets:
            sock.sendto(message + "\n", t)
            
        print "UDP Sent:", message
    except Exception as e:
        print "UDP Error:", e

def main():
    print "Starting Input Forwarder on", INPUT_DEVICE
    sys.stdout.flush()
    while True:
        try:
            f = open(INPUT_DEVICE, "rb")
            print "Opened device. Listening..."
            sys.stdout.flush()
            while True:
                data = f.read(EVENT_SIZE)
                if data:
                    (tv_sec, tv_usec, type, code, value) = struct.unpack(EVENT_FORMAT, data)
                    if type == 1 and (value == 1 or value == 2):
                        print "Key pressed:", code
                        sys.stdout.flush()
                        send_udp("my_input:%d" % code)
        except Exception as e:
            print "Error:", e
            sys.stdout.flush()
            time.sleep(5)

if __name__ == "__main__":
    main()
