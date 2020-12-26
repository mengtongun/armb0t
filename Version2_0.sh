echo "Starting...."

# preparation work: remove existing files
rm -f /home/pi/camera/OpenCV_detection/ServoRotation/Version2_0/positions.txt
rm -f /home/pi/camera/OpenCV_detection/ServoRotation/Version2_0/image.jpg


# identify the center and redirect result to positions.txt
echo "Capturing Image..."
fswebcam -r 640x480 --no-banner /home/pi/camera/OpenCV_detection/ServoRotation/Version2_0/image.jpg
echo "Finished Capturing Image..."


echo "Detecting Circles..."
python3 /home/pi/camera/OpenCV_detection/ServoRotation/Version2_0/circle_detect_2.0.py >> /home/pi/camera/OpenCV_detection/ServoRotation/Version2_0/positions.txt
echo "Finished Detecting Circles..."

# move the robot_arm to the desired position
echo "Moving Robot Arm..."
python3 /home/pi/camera/OpenCV_detection/ServoRotation/Version2_0/move_arm.py
echo "Finished..."
