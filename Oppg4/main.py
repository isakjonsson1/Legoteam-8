#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time
import threading 

from config import *

ev3 = EV3Brick()
left_motor = Motor(port=Port.A)
right_motor = Motor(port=Port.B)
ultrasonic_sensor = UltrasonicSensor(port=Port.S3)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=82.1)
back_color_sensor = ColorSensor(port=Port.S2)
front_color_sensor = ColorSensor(port=Port.S1)


# Write your program here.
def main():
    # Drive while distance to foreign object is more than 100
    ## Ignore for now
    while ultrasonic_sensor.distance() > 100 or True:
        # There are two sensors. The back sensor will steer the robot
        # by following the left side of the black tape. This means that
        # if the robot detects > 80% white, it should turn to the right
        # if the robot detects > 80% black, it should turn to the left

        turn = 0
        if get_brightness(back_color_sensor) > 80:
            turn = TURN_SPEED
        if get_brightness(back_color_sensor) < 20:
            turn = -TURN_SPEED

        if get_brightness(front_color_sensor) > 80:
            # The front sensor is detecting white. SLOW DOWN!
            robot.drive(SLOW, turn)
        else:
            # Shouldn't be turning when we're going FAAAST AF! xD
            robot.drive(FAST, 0)

    robot.stop()
    ev3.speaker.play_file(SoundFile.CHEERING)


def get_brightness(color_sensor):
    """Returns the brightness (black - white) from 0 - 100"""
    # https://www.rapidtables.com/convert/color/rgb-to-hsv.html
    return max(color_sensor.rgb())
    

if __name__ == "__main__":
    main()