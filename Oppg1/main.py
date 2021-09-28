#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
leftMotor = Motor(port=Port.A)
rightMotor = Motor(port=Port.B)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=56, axle_track=82.1)

# Wheel width: 28mm
# test

# Write your program here.
def main():
    #ev3.speaker.beep()

    #ev3.screen.print("Hello world")
    #wait(2000)

    #rektangel(200, 100)

    ev3.speaker.set_speech_options(language="no", voice="croak", speed=None, pitch=None)
    ev3.speaker.set_volume(volume(100%), which='_all_')
    ev3.speaker.say("Ha en fin dag")
    wait(5000)


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
