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

void moveToInit() {
  setAngle(90, BASE);
  setAngle(5, SHOULDER);
  setAngle(160, ELBOW);
  setAngle(100, ROLL);
  setAngle(50 ,PITCH);
  setAngle(100, WRIST);
  setAngle(100, GRIPPER);
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
    
    int index = data.indexOf("@");
    int x_dist = data.substring(0, index).toInt();
    int y_dist = data.substring(index + 1, data.length()).toInt();
    
    setAngle(x_dist, BASE);
  }
}
