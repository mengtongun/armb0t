#include <Servo.h>
Servo myservoA; // BASE
Servo myservoB; // ELBOW
Servo myservoC; // SHOULDER
Servo myservoD; // ROLLER
Servo myservoE; // PITCH
Servo myservoF; // WRIST
Servo myservoG; // GRIPPER

int x_dist = 0;
int y_dist = 0;

int i, pos, myspeed, myshow;
int sea, seb, sec, sed, see, sef, seg;

static int v = 0;

String message = "";
String mycommand = "";    // Capture the commands sent by the serial port #auto: automatic operation #com: computer serial port control #stop: static state
static int mycomflag = 1; // #auto: 2 autorun, #com: 1 computer control #stop: 0 standstill

void myservosetup() // The steering gear is initialized to the waiting state
{
    sea = myservoA.read();
    seb = myservoB.read();
    sec = myservoC.read();
    sed = myservoD.read();
    see = myservoE.read();
    sef = myservoF.read();
    seg = myservoG.read();

    myspeed = 500;
    for (pos = 0; pos <= myspeed; pos += 1)
    {
        myservoA.write(int(map(pos, 1, myspeed, sea, 66)));
        myservoB.write(int(map(pos, 1, myspeed, seb, 90)));
        myservoC.write(int(map(pos, 1, myspeed, sec, 50)));
        myservoD.write(int(map(pos, 1, myspeed, sed, 90)));
        myservoE.write(int(map(pos, 1, myspeed, see, 120)));
        myservoF.write(int(map(pos, 1, myspeed, sef, 90)));
        delay(1);
    }
}

void setup()
{
    pinMode(13, INPUT);
    pinMode(12, INPUT);
    Serial.begin(9600);

    myshow = 0;
    mycomflag = 1;       // The default power-on state of the robotic arm is: 2 automatic operation
    myservoA.attach(3);  // The port that controls the BASE (A) is ~3
    myservoB.attach(5);  // The port that controls the ELBOW (B) is ~5
    myservoC.attach(6);  // The port that controls the SHOULDER (C) is ~6
    myservoD.attach(9);  // The port that controls the ROLLER rotation (D) is ~9
    myservoE.attach(10); // The port that controls the PITCH (E) is ~10
    myservoF.attach(11); // The port that controls the WRIST (F) is ~11
    myservoG.attach(2);  // The port that controls the eGRIPPER(G) is ~2

    moveToInit();
}

void moveToInit()
{
    myservoA.write(90);  // BASE
    myservoB.write(150); // ELBOW
    myservoC.write(40);  // SHOULDER
    myservoD.write(95);  // ROLLER
    myservoE.write(20);  // PITCH
    myservoF.write(100); // WRIST
    myservoG.write(40);  // GRIPPER
}

void moveToBin(String color)
{

    //   setAngle(90,ELBOW);
    //  myservoB.write(60);

    if (color == "red")
    {
        myservoA.write(200); // move to position of red bin
    }
    else if (color == "green")
    {
        myservoA.write(150); // move to position of green bin
    }
    else if (color == "blue")
    {
        myservoA.write(25); // move to position blue bin
    }
    else if (color == "yellow")
    {
        myservoA.write(0); // move to position of yellow bin
    }
    else
    {
    }
}

void loop()
{
    if (Serial.available() > 0)
    {

        String message = Serial.readStringUntil('\n');

        if (message == "moveToInit")
        {
            moveToInit();
        }
        else if (message == "openGripper")
        {
            myservoG.write(50);
        }
        else if (message == "closeGripper")
        {
            myservoG.write(140);
        }
        else if (message == "setRoll")
        {
            myservoD.write(100);
        }
        else if (message == "setPitch")
        {
            myservoE.write((y_dist * 2) + 10);
        }
        else if (message == "setWrist")
        {
            myservoF.write(100);
        }
        else if (message == "moveToRedBin")
        {
            moveToBin("red");
        }
        else if (message == "moveToGreenBin")
        {
            moveToBin("green");
        }
        else if (message == "moveToBlueBin")
        {
            moveToBin("blue");
        }
        else if (message == "moveToYellowBin")
        {
            moveToBin("yellow");
        }
        else if (message == "moveDown")
        {
            myservoB.write(y_dist - 10);
            //  setAngle(y_dist - 10, ELBOW);
        }
        else if (message == "gripGreenObject")
        {
            myservoA.write(100); // moveBase
            delay(1000);
            myservoB.write(50); // moveElbow
            delay(1000);
            myservoC.write(55); // moveShoulder
            delay(1000);
            myservoB.write(45); // moveElbow
            delay(1000);
            myservoG.write(140); // moveCloseGrip
            delay(1000);
            moveToBin("green");
            delay(1000);
            myservoG.write(40); // moveCloseGrip
            //  setAngle(y_dist - 10, ELBOW);
        }
        else if (message == "gripRedObject")
        {
            myservoA.write(50); // moveBase
            delay(2000);
            myservoB.write(50); // moveElbow
            delay(2000);
            myservoC.write(55); // moveShoulder
            delay(2000);
            myservoB.write(45); // moveElbow
            delay(1000);
            myservoG.write(140); // moveCloseGrip
            delay(1000);
            moveToBin("red");
            delay(1000);
            myservoG.write(40); // moveCloseGrip

            //  setAngle(y_dist - 10, ELBOW);
        }
        else if (message == "gripBlueObject")
        {
            myservoA.write(80); // moveBase
            delay(1000);
            myservoB.write(50); // moveElbow
            delay(1000);
            myservoC.write(55); // moveShoulder
            delay(1000);
            myservoB.write(45); // moveElbow
            delay(1000);
            myservoG.write(140); // moveCloseGrip
            delay(1000);
            moveToBin("blue");
            delay(1000);
            myservoG.write(40); // moveCloseGrip
            //  setAngle(y_dist - 10, ELBOW);
        }
        else if (message == "gripYellowObject")
        {
            myservoA.write(125); // moveBase
            delay(1000);
            myservoB.write(50); // moveElbow
            delay(1000);
            myservoC.write(55); // moveShoulder
            delay(1000);
            myservoB.write(45); // moveElbow
            delay(1000);
            myservoG.write(150); // moveCloseGrip
            delay(1000);
            moveToBin("yellow");
            delay(1000);
            myservoG.write(40); // moveCloseGrip
            //  setAngle(y_dist - 10, ELBOW);
        }
        else
        {
            int index = message.indexOf(":");
            int degree = message.substring(0, index).toInt();
            String servo = message.substring(index + 1, message.length() - 1);

            if (servo == "BASE")
            {
                x_dist = degree;
                //  setAngle(x_dist, BASE);
                myservoA.write(x_dist);
            }
            else if (servo == "ELBOW")
            {
                y_dist = degree;
                myservoB.write(y_dist);
                //  setAngle(y_dist, ELBOW);
            }
            else if (servo == "SHOULDER")
            {
                myservoC.write(degree);
                //  setAngle(degree, SHOULDER);
            }
            else if (servo == "PITCH")
            {
                myservoE.write(degree);
                //  setAngle(degree, PITCH);
            }
            else if (servo == "ROLL")
            {
                myservoD.write(degree);
                //  setAngle(degree, ROLL);
            }
            else if (servo == "WRIST")
            {
                myservoA.write(degree);
                //  setAngle(degree, WRIST);
            }
            else
            {
            }
        }
        Serial.print("You Sent Me: ");
        Serial.println(message);
    }
}