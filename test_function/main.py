#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
pen = Motor(port=Port.D, positive_direction=Direction.CLOCKWISE)
leftMotor = Motor(port=Port.A)
rightMotor = Motor(port=Port.B)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=56, axle_track=82.1)
SPEED = 500;
SKALAR = 10;
# Write your program here
def main():
    t0 = time.time()
    t1 = t0-time.time()+3

    while t1 > -3:
        print(t1)
        t1 = t0-time.time()+3
        robot.drive(SPEED, functionDerivative(t1))



def drive(avstand):
    wait(100)
    robot.straight(-avstand)
    wait(100)

def turn(vinkel):
    robot.turn(vinkel)

def hev():
    pen.run_target(360, 270, then=Stop.HOLD, wait=True)

def senk():
    pen.run_target(-360, 0, then=Stop.HOLD, wait=True)

def rektangel(x, y):
    drive(x)
    turn(90)
    drive(y)
    turn(90)
    drive(x)
    turn(90)
    drive(y)
    turn(90)

def functionDerivative(x):
    return 2*x*SKALAR

def distance(time):
    return SPEED*time


if __name__ == "__main__":
    main()
