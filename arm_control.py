
import serial
import time
import numpy as np

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


def convert(max_px, xy, max_degree):
    return (xy * max_degree) // max_px


def setAngle(ser, msg, timeout):
    ser.write(msg.encode())
    time.sleep(timeout)
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(timeout)


def move_arm_bot(x, y, color):
    x_dist = convert(640, x, 180)
    y_dist = convert(480, y, 90)
    print('x_dist: ', x_dist)
    print('y_dist: ', y_dist)
    print('color: ', color)
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    setAngle(ser, init_msg, 1)

    #setAngle(ser, str(x_dist + 7) + ':BASE@', 1)
    if x_dist <= 90:
        setAngle(ser, str(x_dist + 5) + ':BASE@', 1)
    else:
        setAngle(ser, str(x_dist - 3) + ':BASE@', 1)

    setAngle(ser, str(MAGIC_NUM) + ':ELBOW@', 1)

    setAngle(ser, open_gripper_msg, 1)

    setAngle(ser, str(MAGIC_NUM) + ':SHOULDER@', 1)

    setAngle(ser, str(MAGIC_NUM - 10) + ':ELBOW@', 1)

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
