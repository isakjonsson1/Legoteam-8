#!/usr/bin/env pybricks-micropython
from config import *


def main():
    square(100)


def square(mm):
    # Checks if the robot is calibrated by driving a square with length n cm.
    drive_base.straight(mm)
    drive_base.turn(90)
    drive_base.straight(mm)
    drive_base.turn(90)
    drive_base.straight(mm)
    drive_base.turn(90)
    drive_base.straight(mm)
    drive_base.turn(90)


def drive(mm):
    drive_base.straight(mm)


def threesixty():
    drive_base.turn(360)


if __name__ == "__main__":
    main()


from time import sleep

sleep(1)
drive_base.turn(11720)
