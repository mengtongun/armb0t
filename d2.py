# import the necessary packages
import numpy as np
import cv2
import time
import arm_control as ac


def convert(max_px, xy, max_degree):
    return (xy * max_degree) // max_px


# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red': (166, 84, 141), 'green': (66, 122, 129), 'blue': (
    97, 100, 117), 'yellow': (23, 59, 119)}

upper = {'red': (186, 255, 255), 'green': (86, 255, 255),
         'blue': (117, 255, 255), 'yellow': (54, 255, 255)}

colors = {'red': (0, 0, 255), 'green': (0, 255, 0),
          'blue': (255, 0, 0), 'yellow': (0, 255, 217)}

# camera = cv2.VideoCapture(0)

rgby_circles = {'red': None, 'green': None, 'blue': None, 'yellow': None}

# keep looping
while True:
    # grab the current frame
    frame = cv2.imread('image.jpg')
    frame = cv2.flip(frame, 1)

    # blur the frame, and convert it to the HSV
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            x_dist = convert(640, center[0], 180)
            y_dist = convert(480, center[1], 90)

            rgby_circles[key] = (x_dist, y_dist)

            # only proceed if the radius meets a minimum size. Correct this value for your object's size
            if radius > 0.5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)),
                           int(radius), colors[key], 2)
                cv2.putText(frame, key + " ball", (int(x-radius), int(y-radius)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[key], 2)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):

        if rgby_circles['red'] != None and rgby_circles['green'] != None and rgby_circles['blue'] != None and rgby_circles['yellow'] != None:
            time.sleep(30)

        # cv2.destroyAllWindows()
        # image = cv2.imread('image.jpg')
        # image = cv2.flip(image, 1)
        # for key, value in rgby_circles.items():
        #     print(value, key)
        #     center = rgby_circles[key].split(' ')
        #     cv2.circle(image, (int(center[0]), int(
        #         center[1])), 20, colors[key], 2)
        #     cv2.putText(image, key + " ball", (int(center[0]) - 20, int(
        #         center[1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[key], 2)

        #     cv2.imshow('Image', image)

        key = cv2.waitKey(0) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord('y'):
            for key, value in rgby_circles.items():
                if (value != None):
                    print(value, key)
                    ac.move_arm_bot(value[0], value[1], key)
                    break
            break
        elif key == ord('n'):
            rgby_circles = {'red': None, 'green': None,
                            'blue': None, 'yellow': None}
            cv2.destroyAllWindows()
            time.sleep(1)
            continue
        else:
            pass


# camera.release()
cv2.destroyAllWindows()
