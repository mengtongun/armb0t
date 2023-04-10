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


def convert(max_px, xy, max_degree):
    return (xy * max_degree) // max_px


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


def control_arm_by_color(color):

    color = color.lower()
    print("Color Detect: ", color)

    # ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    # ser.flush()

    setMessage(ser, init_msg, 0.4)

    # setMessage(ser, close_gripper_msg, 1)

    if color == "red":

        # define static base angel for RED color
        setMessage(ser, str(50) + ':BASE@', 0.4)

        static_move_to_grip_object()

        # move to RED BIN
        setMessage(ser, move_to_red_bin_msg, 0.4)

    elif color == "green":

        # define static base angel for GREEN color
        setMessage(ser, str(70) + ':BASE@', 0.4)

        static_move_to_grip_object()

        # move to GREEN BIN
        setMessage(ser, move_to_green_bin_msg, 0.4)

    elif color == "yellow":

        # define static base angel for YELLOW color
        setMessage(ser, str(110) + ':BASE@', 0.4)

        static_move_to_grip_object()

        # move to YELLOW BIN
        setMessage(ser, move_to_yellow_bin_msg, 0.4)

    elif color == "blue":

        # define static base angel for BLUE color
        setMessage(ser, str(135) + ':BASE@', 0.4)

        static_move_to_grip_object()

        # move to BLUE BIN
        setMessage(ser, move_to_blue_bin_msg, 0.4)

    else:
        pass

    setMessage(ser, open_gripper_msg, 0.4)

    setMessage(ser, init_msg, 0.4)

    print("Done sorting object colored:", color)

    ser.flush()


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    if DEBUG_MODE:
        print('DEBUG')
        while True:
            ip = input()
            setMessage(ser, ip, 1)
    else:
        with open("positions.txt", "r") as f:
            lines = f.readlines()
        f.close()

        if len(lines) == 0:
            print('No Circles Detected')
            exit()
        else:
            colors_found = ["red", "blue", "green", "yellow"]
            for i in range(len(lines)):
                # a = np.fromstring((lines[0]), dtype=str, sep=' ')
                # print(a[0], a[1])
                line = lines[i].split(' ')

                x = int(line[0])
                y = int(line[1])
                color = line[2]
                x_dist = convert(640, x, 180)
                y_dist = convert(480, y, 90)

                if color in colors_found:
                    continue
                else:
                    colors_found.append(color)

                print("********", x_dist, y_dist, color, "**********")

                setMessage(ser, init_msg, 1)

                # setMessage(ser, str(x_dist + 7) + ':BASE@', 1)
                # if x_dist <= 90:

                #     setMessage(ser, str(x_dist + 5) + ':BASE@', 1)

                # else:

                #     setMessage(ser, str(x_dist - 3) + ':BASE@', 1)

                # Check detected color:
                if color == "red\n":

                    # define static base angel for RED color
                    setMessage(ser, str(50) + ':BASE@', 1)

                    static_move_to_grip_object()

                    # move to RED BIN
                    setMessage(ser, move_to_red_bin_msg, 1)

                elif color == "green\n":

                    # define static base angel for GREEN color
                    setMessage(ser, str(70) + ':BASE@', 1)

                    static_move_to_grip_object()

                    # move to GREEN BIN
                    setMessage(ser, move_to_green_bin_msg, 1)

                elif color == "yellow\n":

                    # define static base angel for YELLOW color
                    setMessage(ser, str(110) + ':BASE@', 1)

                    static_move_to_grip_object()

                    # move to YELLOW BIN
                    setMessage(ser, move_to_yellow_bin_msg, 1)

                elif color == "blue\n":

                    # define static base angel for BLUE color
                    setMessage(ser, str(135) + ':BASE@', 1)

                    static_move_to_grip_object()

                    # move to BLUE BIN
                    setMessage(ser, move_to_blue_bin_msg, 1)

                else:
                    pass

                # setMessage(ser, str(90) + ':ELBOW@', 1)

                # setMessage(ser, open_gripper_msg, 1)

                # setMessage(ser, str(65) + ':SHOULDER@', 1)

                # setMessage(ser, str(60) + ':ELBOW@', 1)

                # setMessage(ser, str(70) + ':SHOULDER@', 1)

                # setMessage(ser, close_gripper_msg, 1)

                # if color == 'red\n':
                #     # setMessage(ser,gripRedObj,1)
                #     print(gripRedObj)
                #     setMessage(ser, move_to_red_bin_msg, 1)
                # elif color == 'green\n':
                #     print(gripGreenObj)
                #     # setMessage(ser,gripGreenObj,1)
                #     setMessage(ser, move_to_green_bin_msg, 1)
                # elif color == 'blue\n':
                #     print(gripBlueObj)
                #     # setMessage(ser,gripBlueObj,1)
                #     setMessage(ser, move_to_blue_bin_msg, 1)
                # elif color == 'yellow\n':
                #     print(gripRedObj)
                #     # setMessage(ser,gripYellowObj,1)
                #     setMessage(ser, move_to_yellow_bin_msg, 1)
                # else:
                #     pass

                setMessage(ser, open_gripper_msg, 1)

                setMessage(ser, init_msg, 1)

        print('exit')

        ser.flush()
