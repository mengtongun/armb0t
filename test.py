import serial
import time
import numpy as np


DEBUG_MODE = True


init_msg = 'moveToInit\n'
open_gripper_msg = 'openGripper\n'
close_gripper_msg = 'closeGripper\n'
roll_msg = 'setRoll\n'
pitch_msg = 'setPitch\n'
wrist_msg = 'setWrist\n'
move_to_red_bin_msg = 'moveToRedBin\n'
move_to_green_bin_msg = 'moveToGreenBin\n'
move_to_blue_bin_msg = 'moveToBlueBin\n'
move_to_yellow_bin_msg = 'moveToYellowBin\n'
move_down_msg = 'moveDown\n'


#offset_x = -10
#offset_y = -20

MAGIC_NUM = 15
#OFFSET_RIGHT = 10
#OFFSET_LEFT = 30


def setAngle(ser, msg, timeout):
    ser.write(msg.encode())
    time.sleep(timeout)
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(timeout)
    
    
def convert(max_px, xy, max_degree):
    return (xy * max_degree) // max_px


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    
    
    if DEBUG_MODE:
        print('DEBUG')
        while True:
            ip = input()
            setAngle(ser, ip, 1)
