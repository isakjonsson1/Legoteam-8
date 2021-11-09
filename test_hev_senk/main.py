#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
hev_og_senk = Motor(port=Port.D, positive_direction=Direction.CLOCKWISE)
leftMotor = Motor(port=Port.A)
rightMotor = Motor(port=Port.B)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=56, axle_track=82.1)

# Write your program here
def main():
    hev_og_senk.run_target(360, 270, then=Stop.HOLD, wait=True)
    rektangel(500, 500)
    hev_og_senk.run_target(-360, 0, then=Stop.HOLD, wait=True)


def drive(avstand):
    wait(100)
    robot.straight(-avstand)
    wait(100)

def turn(vinkel):
    robot.turn(vinkel)

def rektangel(x, y):
    drive(x)
    turn(90)
    drive(y)
    turn(90)
    drive(x)
    turn(90)
    drive(y)
    turn(90)

if __name__ == "__main__":
    main()
