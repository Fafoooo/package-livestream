#!/usr/bin/python
import struct
import socket
import sys
import time

# Usually event0 is the main keyboard (Presenter PageUp/Down)
INPUT_DEVICE = "/dev/input/event1" 
UDP_IP = "127.0.0.1"
UDP_PORT = 4444

# Event structure for 32-bit (typical Pi). 
# struct input_event { long time[2]; unsigned short type; unsigned short code; long value; }
# 'l' = 4 bytes, 'H' = 2 bytes, 'i' = 4 bytes. Total 16 bytes.
EVENT_FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

def send_udp(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, (UDP_IP, UDP_PORT))
    except Exception as e:
        print("UDP Error: %s" % e)

def main():
    print("Starting Input Forwarder on %s..." % INPUT_DEVICE)
    sys.stdout.flush()
    while True:
        try:
            f = open(INPUT_DEVICE, "rb")
            print("Opened device. Listening...")
            sys.stdout.flush()
            while True:
                data = f.read(EVENT_SIZE)
                if data:
                    # In case of partial reads or size mismatch, unpack might fail.
                    # We rely on correct alignment.
                    (tv_sec, tv_usec, type, code, value) = struct.unpack(EVENT_FORMAT, data)
                    
                    # Type 1 = EV_KEY. Value 1 = Pressed, 2 = Repeat
                    if type == 1 and (value == 1 or value == 2):
                        print("Key pressed: %d" % code)
                        sys.stdout.flush()
                        send_udp("input:%d" % code)
        except Exception as e:
            print("Error: %s" % e)
            sys.stdout.flush()
            time.sleep(5)

if __name__ == "__main__":
    main()
