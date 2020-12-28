#include<Wire.h>
#include<Adafruit_PWMServoDriver.h>

#define MIN_PULSE_WIDTH 650
#define MAX_PULSE_WIDTH 2350
#define OFFSET 1500
#define FREQUENCY 50

// Instantiate the Adafruit driver class
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int BASE = 0;
int ELBOW = 1;
int SHOULDER = 2;
int ROLL = 3;
int PITCH = 4;
int WRIST = 5;
int GRIPPER = 6;

int x_dist = 0;
int y_dist = 0;

void moveToInit() {
  setAngle(90, BASE);
  setAngle(5, SHOULDER);
  setAngle(160, ELBOW);
  setAngle(100, ROLL);
  setAngle(0 ,PITCH);
  setAngle(100, WRIST);
  setAngle(100, GRIPPER);
}

void moveToBin(String color) {
  setAngle(90,ELBOW);
  delay(500);
  if (color == "red") {
    setAngle(200, BASE);
  } else if (color == "green") {
    setAngle(175, BASE);
  } else if (color == "blue") {
    setAngle(150, BASE);
  } else if (color == "yellow") {
    setAngle(125, BASE);
  } else {}
  setAngle(45, ELBOW);
}

void setup() {
    pwm.begin();
    Serial.begin(9600);
    pwm.setPWMFreq(FREQUENCY);
    moveToInit();
}

// Method for angle munipulation on the Servo
void setAngle(int angle, int servoOut) {
    int pulse_wide, pulse_width;

    // convert to pulse width
    pulse_wide = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
    pulse_width = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);

    // Control Servo
    pwm.setPWM(servoOut, 0, pulse_width);
} 

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    if (data == "moveToInit") {
        moveToInit();
      } else if (data == "openGripper") {
          setAngle(700, GRIPPER);
      } else if (data == "closeGripper") {
          setAngle(100, GRIPPER);
      } else if (data == "setRoll") {
          setAngle(100, ROLL);
      } else if (data == "setPitch") {
          setAngle((y_dist * 2) + 10, PITCH);
      } else if (data == "setWrist") {
          setAngle(100, WRIST);
      } else if (data == "moveToRedBin") {
          moveToBin("red");
      } else if (data == "moveToGreenBin") {
          moveToBin("green");
      } else if (data == "moveToBlueBin") {
          moveToBin("blue");
      } else if (data == "moveToYellowBin") {
          moveToBin("yellow");
      } else if (data == "moveDown") {
          //setAngle(10 * cos((x_dist * PI)/180), ELBOW);
          setAngle(y_dist - 10, ELBOW);
      } else {
          int index = data.indexOf(":");
          int degree = data.substring(0, index).toInt();
          String servo = data.substring(index + 1, data.length() - 1);
          
          if (servo == "BASE") {
            x_dist = degree;
            setAngle(x_dist, BASE);
          } else if (servo == "ELBOW") {
            y_dist = degree;
            setAngle(y_dist, ELBOW);
          } else if (servo == "SHOULDER") {
            setAngle(degree, SHOULDER);
          } else if (servo == "PITCH") {
            setAngle(degree, PITCH);
          } else if (servo == "ROLL") {
            setAngle(degree, ROLL);
          } else if (servo == "WRIST") {
            setAngle(degree, WRIST);
          } else {}
      }
      Serial.print("You Sent Me: ");
      Serial.println(data);
  }
}
