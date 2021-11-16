#!/usr/bin/env pybricks-micropython
"""Functions used to calibrate the robot"""
import _thread as thread
import time

from pybricks.parameters import Stop

from robot.config import drive_base, pen_motor, TURN_RATE, TURN_SPEED, PEN_TORQUE


finished = False

def main():
    """Start function"""
    global finished
    print_thread = thread.start_new_thread(print_angle)
    engage_pen()
    finished = True

def print_angle():
    global finished
    angle = pen_motor.angle()
    while not finished:
        print("Angle: {}".format(angle), end="\r")

def square(length):
    """Makes the robot drive in a square with sides length milimeters long"""
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
    pen_motor.run_angle(TURN_SPEED, -TURN_RATE, then=Stop.HOLD, wait=True)


def calibrate_pen():
    """Used to calibrate pen"""
    pen_motor.run_until_stalled(-TURN_SPEED, then=Stop.COAST, duty_limit=PEN_TORQUE)
    pen_motor.run_angle(TURN_SPEED, -TURN_RATE, then=Stop.COAST, wait=True)


if __name__ == "__main__":
    main()
