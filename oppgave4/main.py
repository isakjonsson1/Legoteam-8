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
button = TouchSensor(port=Port.S3)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=82.1)
back_color_sensor = ColorSensor(port=Port.S2)
front_color_sensor = ColorSensor(port=Port.S1)


# Write your program here.
def main():
    wait_for_button(button)

    max_brightness = {
       "front": get_brightness(front_color_sensor),
       "back": get_brightness(back_color_sensor)
    }
    # 3/4 av gjennomsnittet av de to sensorene
    WHITE_TRESH = sum(max_brightness.values()) * 3 / 8

    wait_for_button(button)

    # Drive while distance to foreign object is more than 100
    ## Ignore for now
    state = None
    turn = 0
    while True:
        
        # There are two sensors. The back sensor will steer the robot
        # by following the left side of the black tape. This means that
        # if the robot detects > 80% white, it should turn to the right
        # if the robot detects > 80% black, it should turn to the left
        
        brightness = get_brightness(back_color_sensor)
       
        if get_brightness(front_color_sensor) < BLACK_THRESH:
            # Black ahead! Goooo faaaAaast !!!!!
            if state != "STRAIGHT":
                robot.drive(FAST, 0)
                turn = 0
                state = "STRAIGHT"
        else:
            # White ahead, we should probably be cautious...
            if brightness > WHITE_THRESH:
                # Too much white!
                # Slowly increment turn speed if the car is off-track
                if state != "LEFT":
                    turn = TURN_MIN
                    state = "LEFT"
                else:
                    turn = min(turn + TURN_INC, TURN_MAX)
            if brightness < BLACK_THRESH:
                # Too much black!
                # Slowly increment turn speed if the car is off-track
                if state != "RIGHT":
                    turn = -TURN_MIN
                    state = "RIGHT"
                else:
                    turn = max(turn - TURN_INC, -TURN_MAX)

            # ev3.screen.print(state, turn)
            robot.drive(SLOW, turn)



def get_brightness(color_sensor):
    """Returns the brightness (black - white) from 0 - 255"""
    # https://www.rapidtables.com/convert/color/rgb-to-hsv.html
    return max(color_sensor.rgb())

def wait_for_button(button):
    # Waits until button is pressed
    while not button.pressed():
        pass

    # Waits until button is released
    while button.pressed():
        pass
    

if __name__ == "__main__":
    main()