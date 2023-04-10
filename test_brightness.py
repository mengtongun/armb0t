import numpy as np
import cv2

# cap = cv2.VideoCapture(0)
camera = cv2.VideoCapture()
camera.open('/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_6C5E18EF-video-index0')

# while(True):
#     # Capture frame-by-frame
#     ret, frame = camera.read()
#     cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# # When everything done, release the capture
# camera.release()
# cv2.destroyAllWindows()

while(True):
    # Capture frame-by-frame
    ret, frame = camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    contrast = 1.25
    brightness = 100
    frame[:,:,2] = np.clip(contrast * frame[:,:,2] + brightness, 0, 255)
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()