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
    else:
        with open("/home/pi/camera/OpenCV_detection/ServoRotation/Version2_0/positions.txt", "r") as f:
            lines = f.readlines()
        f.close()
    
        if len(lines) == 0:
            print('No Circles Detected')
            exit()
        else:
            colors_found = []
            for i in range(len(lines)):
                #a = np.fromstring((lines[0]), dtype=str, sep=' ')
                #print(a[0], a[1])
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
            
                print(x_dist, y_dist, color)
                
                setAngle(ser, init_msg, 1)
                
                setAngle(ser, str(x_dist) + ':BASE@\n', 1)
                
                setAngle(ser, str(y_dist) + ':ELBOW@\n', 1)
                
                setAngle(ser, str(y_dist) + ':SHOULDER@\n', 1)
                
                setAngle(ser, roll_msg, 1)
                
                setAngle(ser, pitch_msg, 1)
    
                setAngle(ser, wrist_msg, 1)
                
                setAngle(ser, open_gripper_msg, 1)
                
                setAngle(ser, move_down_msg, 1)
                
                setAngle(ser, close_gripper_msg, 0.5)
                
                if color == 'red\n':
                    setAngle(ser, move_to_red_bin_msg, 1)
                elif color == 'green\n':
                    setAngle(ser, move_to_green_bin_msg, 1)
                elif color == 'blue\n':
                    setAngle(ser, move_to_blue_bin_msg, 1)
                else:
                    pass
                
                time.sleep(2)
                
                setAngle(ser, init_msg, 1)
                
        print('exit')
        
        ser.flush()