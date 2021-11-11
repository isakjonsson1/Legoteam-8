#!/usr/bin/env pybricks-micropython
"""Functions used to calibrate the robot"""
from config import *
from pybricks.parameters import Stop
import time
def main():
    """Start function"""

    calibrate_pen()
    time.sleep(1)
    lift_pen()
    time.sleep(1)
    engage_pen()

def square(length):
    """Makes the robot drive in a square with sides length milimeters long"""
    # Checks if the robot is calibrated by driving a square with length n cm.
    drive_base.straight(length)
    drive_base.turn(90)
    drive_base.straight(length)
    drive_base.turn(90)
    drive_base.straight(length)
    drive_base.turn(90)
    drive_base.straight(length)
    drive_base.turn(90)


def drive(length):
    """Drives straight for length milimeters"""
    drive_base.straight(length)


def threesixty():
    """Turns 360 degrees"""
    drive_base.turn(360)

def engage_pen():
    """Puts the pen on the paper"""
  
    pen_motor.run_until_stalled(TURN_SPEED, then=Stop.COAST, duty_limit=PEN_TORQUE)

    

def lift_pen():
    """Lifts the pen from the paper"""
   
    pen_motor.run_angle(TURN_SPEED, TURN_RATE, then=Stop.HOLD, wait=True)

    
def calibrate_pen():
    pen_motor.run_until_stalled(TURN_SPEED, then=Stop.COAST, duty_limit=PEN_TORQUE)
    pen_motor.run_angle(TURN_SPEED, -TURN_RATE, then=Stop.COAST, wait=True)


if __name__ == "__main__":
    main()
