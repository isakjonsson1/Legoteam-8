#!/usr/bin/env pybricks-micropython
"""Functions used to calibrate the robot"""
from config import drive_base


def main():
    """Start function"""
    square(100)


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


if __name__ == "__main__":
    main()
