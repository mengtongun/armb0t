import cv2
import numpy as np

# set color ranges for red, green, blue, and yellow
lower = {'red': (0, 50, 50), 'green': (36, 50, 50),
         'blue': (100, 50, 50), 'yellow': (22, 50, 50)}
upper = {'red': (10, 255, 255), 'green': (86, 255, 255),
         'blue': (130, 255, 255), 'yellow': (40, 255, 255)}
colors = {'red': (0, 0, 255), 'green': (0, 255, 0),
          'blue': (255, 0, 0), 'yellow': (0, 255, 217)}

# open the default camera
cap = cv2.VideoCapture(0)

while True:
    # read frame from camera
    ret, frame = cap.read()

    # convert frame to HSV format
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_colors = []  # initialize list to store detected colors

    # loop through each color and detect corresponding circles
    for color_name, color_code in colors.items():
        mask = cv2.inRange(hsv, lower[color_name], upper[color_name])
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # detect circle by fitting contour to a minimum enclosing circle
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                # draw circle around the detected object
                cv2.circle(frame, (int(x), int(y)), int(radius), color_code, 2)
                # add detected color to list
                detected_colors.append(color_name)

    # display live image with detected circles
    cv2.imshow('Live Detection', frame)

    # wait for user to press key
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()

# print detected colors as array
print(detected_colors)
