#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random 
import time
import threading 

from config import *

ev3 = EV3Brick()
left_motor = Motor(port=Port.A)
right_motor = Motor(port=Port.B)
ultrasonic_sensor = UltrasonicSensor(port=Port.S3)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=56, axle_track=82.1)
back_color_sensor = ColorSensor(port=Port.S2)
front_color_sensor = ColorSensor(port=Port.S1)


# Write your program here.
def main():
    thread: threading.Thread = threading.Thread(
        target=ev3.speaker.play_file,
        args=(SoundFile.FANFARE,)
    )
    thread.start()

    # Drive while distance to foreign object is more than 100
    while ultrasonic_sensor.distance() > 100:
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
            robot.drive(FAST)
            if not thread.is_alive()
                thread: threading.Thread = threading.Thread(
                    target=ev3.speaker.play_file,
                    args=(SoundFile.FANFARE,)
                )
                thread.start()

    robot.stop()
    ev3.speaker.play_file(SoundFile.CHEERING)


def get_brightness(color_sensor):
    """Returns the brightness (black - white) from 0 - 100"""

    # .color returnerer HSV-farge hvor V = brightness value fra 0 - 100
    # H = Hue og er fra 0 - 360 ()
    # S = Saturation og er fra 0 - 100 (100 = sterk farge, 0 = svart-hvitt)
    return color_sensor.color().v
    

if __name__ == "__main__":
    main()