import serial
import time
import numpy as np


DEBUG_MODE = False


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

gripGreenObj = "gripGreenObject\n"
gripRedObj = "gripRedObject\n"
gripYellowObj = "gripYellowObject\n"
gripBlueObj = "gripBlueObject\n"


# offset_x = -10
# offset_y = -20

MAGIC_NUM = 50
# OFFSET_RIGHT = 10
# OFFSET_LEFT = 30

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()


def setMessage(ser, msg, timeout):
    ser.write(msg.encode())
    time.sleep(timeout)
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(timeout)


def static_move_to_grip_object():
    setMessage(ser, str(90) + ':ELBOW@', 0.4)

    # setMessage(ser, open_gripper_msg, 1)

    setMessage(ser, str(65) + ':SHOULDER@', 0.4)

    # setMessage(ser, str(MAGIC_NUM - 10) + ':ELBOW@', 1)
    setMessage(ser, str(60) + ':ELBOW@', 0.4)
    setMessage(ser, str(70) + ':SHOULDER@', 0.4)
    # setMessage(ser, str(90) + ':ELBOW@', 1)

    setMessage(ser, close_gripper_msg, 0.4)

    setMessage(ser, str(90) + ':ELBOW@', 0.4)
    setMessage(ser, str(50) + ':SHOULDER@', 0.4)


colorList = ['red', 'green', 'blue', 'yellow']
while True:
    # for color in colorList:

    setMessage(ser, init_msg, 1)

    # define static base angel for RED color
    setMessage(ser, str(50) + ':BASE@', 0.4)

    static_move_to_grip_object()

    # move to RED BIN
    setMessage(ser, move_to_red_bin_msg, 1)

    setMessage(ser, init_msg, 1)

    # define static base angel for GREEN color
    setMessage(ser, str(70) + ':BASE@', 0.4)

    static_move_to_grip_object()

    # move to GREEN BIN
    setMessage(ser, move_to_green_bin_msg, 1)

    setMessage(ser, init_msg, 1)

    # define static base angel for YELLOW color
    setMessage(ser, str(110) + ':BASE@', 0.4)

    static_move_to_grip_object()

    # move to YELLOW BIN
    setMessage(ser, move_to_yellow_bin_msg, 1)

    setMessage(ser, init_msg, 1)

    # define static base angel for BLUE color
    setMessage(ser, str(135) + ':BASE@', 0.4)

    static_move_to_grip_object()

    # move to BLUE BIN
    setMessage(ser, move_to_blue_bin_msg, 1)

    setMessage(ser, init_msg, 1)
    # setMessage(ser, open_gripper_msg, 1)

    print('exit')

    ser.flush()
