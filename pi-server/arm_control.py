
import serial
import time
import numpy as np

SERIAL_PORT = '/dev/tty.usbmodem1201'

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

MAGIC_NUM = 55
OFFSET_RIGHT = 10
OFFSET_LEFT = 30


def convert(max_px, xy, max_degree):
    return (xy * max_degree) // max_px


def setAngle(ser, msg, timeout):
    ser.write(msg.encode())
    time.sleep(timeout)
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(timeout)


debug = True


def move_arm_bot(x, y, color):
    try:
        x_dist = x
        y_dist = y
        print('x_dist: ', x_dist)
        print('y_dist: ', y_dist)
        print('color: ', color)
        ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
        ser.flush()
        setAngle(ser, init_msg, 1)

        #setAngle(ser, str(x_dist + 7) + ':BASE@', 1)
        if x_dist <= 90:
            setAngle(ser, str(x_dist+OFFSET_LEFT) + ':BASE@', 1)
        else:
            setAngle(ser, str(x_dist - OFFSET_RIGHT) + ':BASE@', 1)

        setAngle(ser, str(MAGIC_NUM) + ':ELBOW@', 1)

        setAngle(ser, open_gripper_msg, 1)

        setAngle(ser, str(MAGIC_NUM) + ':SHOULDER@', 1)

        setAngle(ser, str(MAGIC_NUM - 5) + ':ELBOW@', 1)

        setAngle(ser, close_gripper_msg, 1)

        if color == 'red':
            print("Move to red bin")
            setAngle(ser, move_to_red_bin_msg, 1)
        elif color == 'green':
            setAngle(ser, move_to_green_bin_msg, 1)
        elif color == 'blue':
            setAngle(ser, move_to_blue_bin_msg, 1)
        elif color == 'yellow':
            setAngle(ser, move_to_yellow_bin_msg, 1)
        else:
            pass

        setAngle(ser, open_gripper_msg, 1)

        setAngle(ser, init_msg, 1)
        print('exit')

        ser.flush()
        return True
    except:
        return False


def move_to_base():
    try:
        ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
        ser.flush()
        setAngle(ser, init_msg, 1)
        return True
    except:
        return False


def pick_red_static():
    try:
        ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
        ser.flush()
        setAngle(ser, init_msg, 1)
        setAngle(ser, str(90) + ':BASE@', 1)
        setAngle(ser, str(MAGIC_NUM) + ':ELBOW@', 1)
        setAngle(ser, open_gripper_msg, 1)
        setAngle(ser, str(MAGIC_NUM) + ':SHOULDER@', 1)
        setAngle(ser, str(MAGIC_NUM - 5) + ':ELBOW@', 1)
        setAngle(ser, close_gripper_msg, 1)
        setAngle(ser, move_to_red_bin_msg, 1)
        setAngle(ser, open_gripper_msg, 1)
        setAngle(ser, init_msg, 1)
        return True
    except:
        return False
