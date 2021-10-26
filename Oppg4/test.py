#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

ev3 = EV3Brick()
left_motor = Motor(port=Port.A)
right_motor = Motor(port=Port.B)
button = TouchSensor(port=Port.S3)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=82.1)
back_color_sensor = ColorSensor(port=Port.S2)
front_color_sensor = ColorSensor(port=Port.S1)


while True:
    ev3.screen.print("f: " + str(get_brightness(front_color_sensor)) + "b: " + str(get_brightness(back_color_sensor)))

def get_brightness(color_sensor):
    """Returns the brightness (black - white) from 0 - 255"""
    # https://www.rapidtables.com/convert/color/rgb-to-hsv.html
    return max(color_sensor.rgb())