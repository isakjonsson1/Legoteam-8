#!/usr/bin/env pybricks-micropython
"""Functions used to calibrate the robot"""
import _thread as thread

from robot import Robot

bot = Robot(scale=1)

finished = False

def main():
    """Start function"""
    global finished
    # print_thread = thread.start_new_thread(print_angle, (), {})
    bot.calibrate_pen()
    finished = True

def print_angle():
    global finished
    angle = bot.pen_motor.angle()
    while not finished:
        print("Angle: {}".format(angle), end="\r")

def square(length):
    """Makes the robot drive in a square with sides length milimeters long"""
    bot.drive_base.straight(length)
    bot.drive_base.turn(90)
    bot.drive_base.straight(length)
    bot.drive_base.turn(90)
    bot.drive_base.straight(length)
    bot.drive_base.turn(90)
    bot.drive_base.straight(length)
    bot.drive_base.turn(90)


def drive(length):
    """Drives straight for length milimeters"""
    bot.drive_base.straight(length)


def threesixty():
    """Turns 360 degrees"""
    bot.drive_base.turn(360)

if __name__ == "__main__":
    main()
