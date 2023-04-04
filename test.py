import serial
import time
import numpy as np


DEBUG_MODE = True


def setAngle(ser, msg, timeout):
    ser.write(msg.encode())
    time.sleep(timeout)
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(timeout)


def convert(max_px, xy, max_degree):
    return (xy * max_degree) // max_px


if __name__ == '__main__':
    ser = serial.Serial('/dev/tty.usbmodem1201', 9600, timeout=1)
    ser.flush()

    if DEBUG_MODE:
        print('DEBUG')
        while True:
            ip = input()
            setAngle(ser, ip, 1)
# str(10) + ':BASE@'
