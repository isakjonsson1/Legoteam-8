#!/usr/bin/env pybricks-micropython
"""Functions used to calibrate the robot"""
from config import drive_base, pen_motor
from pybricks.parameters import Stop

def main():
    """Start function"""


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
  
    pen_motor.run_target(100, -360, then=Stop.HOLD, wait=True)

    

def lift_pen():
    """Lifts the pen from the paper"""
   
    pen_motor.run_target(100, -270, then=Stop.HOLD, wait=True)

    

if __name__ == "__main__":
    main()
