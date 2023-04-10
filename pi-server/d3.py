import threading
import numpy as np
import cv2
from fastapi import FastAPI

app = FastAPI()

lower = {'red': (166, 84, 141), 'green': (66, 122, 129),
         'blue': (97, 100, 117), 'yellow': (23, 59, 119)}
upper = {'red': (186, 255, 255), 'green': (86, 255, 255),
         'blue': (117, 255, 255), 'yellow': (54, 255, 255)}
colors = {'red': (0, 0, 255), 'green': (0, 255, 0),
          'blue': (255, 0, 0), 'yellow': (0, 255, 217)}
rgby_circles = {'red': None, 'green': None, 'blue': None, 'yellow': None}

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# def convert(size, coord, fov):
#     return np.tan(coord/size*fov/2/180*np.pi)*2

def convert(max_px, xy, max_degree):
    return (xy * max_degree) // max_px


def detect_colors():
    global rgby_circles

    while True:
        _, frame = camera.read()
        frame = cv2.flip(frame, 1)

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        for key, value in upper.items():
            kernel = np.ones((9, 9), np.uint8)
            mask = cv2.inRange(hsv, lower[key], upper[key])
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            cnts = cv2.findContours(
                mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                x_dist = convert(640, center[0], 180)
                y_dist = convert(480, center[1], 90)

                rgby_circles[key] = (x_dist, y_dist)

                if radius > 0.5:
                    cv2.circle(frame, (int(x), int(y)),
                               int(radius), colors[key], 2)
                    cv2.circle(frame, center, 5, colors[key], -1)

        cv2.imshow("Frame", frame)
        print(rgby_circles)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_colors()
