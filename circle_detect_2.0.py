import numpy as np
import cv2
import serial
import time

def convert(max_px, xy, max_degree):
    return (xy * max_degree) // max_px

cap = cv2.VideoCapture(0)

s1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
s1.flush()

circles = {'red': None, 'blue': None, 'yellow': None}

while(True):
    # Capture frame-by-frame
    ret, captured_frame = cap.read()
    output_frame = captured_frame.copy()

    # Convert original image to BGR, since Lab is only available from BGR
    captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
    # First blur to reduce noise prior to color space conversion
    captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
    # Convert to Lab color space, we only need to check one channel (a-channel) for red here
    captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
    # Threshold the Lab image, keep only the red pixels
    # Possible yellow threshold: [20, 110, 170][255, 140, 215]
    # Possible blue threshold: [20, 115, 70][255, 145, 120]
    
    #red
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 150, 150]), np.array([190, 255, 255]))
    
    #blue
    captured_frame_lab_blue = cv2.inRange(captured_frame_lab, np.array([20, 115, 70]), np.array([255, 145, 120]))
    
    #yellow
    captured_frame_lab_yellow = cv2.inRange(captured_frame_lab, np.array([20, 110, 170]), np.array([255, 140, 215]))
    
    #green #not used because inaccurate
    #captured_frame_lab_green = cv2.inRange(captured_frame_lab, np.array([65, 65, 60]), np.array([80, 255, 255]))
    
    # Second blur to reduce more noise, easier circle detection
    captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
    captured_frame_lab_blue = cv2.GaussianBlur(captured_frame_lab_blue, (5, 5), 2, 2)
    captured_frame_lab_yellow = cv2.GaussianBlur(captured_frame_lab_yellow, (5, 5), 2, 2)
    #captured_frame_lab_green = cv2.GaussianBlur(captured_frame_lab_green, (5, 5), 2, 2)
    # Use the Hough transform to detect circles in the image
    red_circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)
    blue_circles = cv2.HoughCircles(captured_frame_lab_blue, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_blue.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)
    yellow_circles = cv2.HoughCircles(captured_frame_lab_yellow, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_yellow.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)
    #green_circles = cv2.HoughCircles(captured_frame_lab_green, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_green.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)

	# If we have extracted a circle, draw an outline
	# We only need to detect one circle here, since there will only be one reference object
    if red_circles is not None:
        red_circles = np.round(red_circles[0, :]).astype("int")
        cv2.circle(output_frame, center=(red_circles[0][0], red_circles[0][1]), radius=red_circles[0][2], color=(0, 255, 0), thickness=2)
        cv2.putText(output_frame, "red_object", (red_circles[0][0] - 75, red_circles[0][1] + red_circles[0][2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1, cv2.LINE_AA)
        
        x_dist = convert(640, red_circles[0][0], 180)
        y_dist = convert(480, red_circles[0][1], 90)
        
        if x_dist == 0 or y_dist == 0:
            pass
        else:
            msg = str(x_dist) + '@' + str(y_dist) + '#RED\n'
            circles['red'] = msg
            s1.write(msg.encode())
            print(msg)
            time.sleep(1)
            
    if blue_circles is not None:
        blue_circles = np.round(blue_circles[0, :]).astype("int")
        cv2.circle(output_frame, center=(blue_circles[0][0], blue_circles[0][1]), radius=blue_circles[0][2], color=(0, 255, 0), thickness=2)
        cv2.putText(output_frame, "blue_object", (blue_circles[0][0] - 75, blue_circles[0][1] + blue_circles[0][2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1, cv2.LINE_AA)
        
        x_dist = convert(640, blue_circles[0][0], 180)
        y_dist = convert(480, blue_circles[0][1], 90)
        
        if x_dist == 0 or y_dist == 0:
            pass
        else:
            msg = str(x_dist) + '@' + str(y_dist) + '#BLUE\n'
            circles['blue'] = msg
            s1.write(msg.encode())
            print(msg)
            time.sleep(1)
            
        if yellow_circles is not None:
            yellow_circles = np.round(yellow_circles[0, :]).astype("int")
            cv2.circle(output_frame, center=(yellow_circles[0][0], yellow_circles[0][1]), radius=yellow_circles[0][2], color=(0, 255, 0), thickness=2)
            cv2.putText(output_frame, "yellow_object", (yellow_circles[0][0] - 75, yellow_circles[0][1] + yellow_circles[0][2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1, cv2.LINE_AA)
            
            x_dist = convert(640, yellow_circles[0][0], 180)
            y_dist = convert(480, yellow_circles[0][1], 90)
            
            if x_dist == 0 or y_dist == 0:
                pass
            else:
                msg = str(x_dist) + '@' + str(y_dist) + '#YELLOW\n'
                circles['yellow'] = msg
                s1.write(msg.encode())
                print(msg)
                time.sleep(1)

    # Display the resulting frame, quit with q
    cv2.imshow('frame', output_frame)
    if circles['red'] != None and circles['blue'] != None and circles['yellow'] != None:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()