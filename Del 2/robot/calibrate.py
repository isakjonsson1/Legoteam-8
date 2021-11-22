#!/usr/bin/env pybricks-micropython
"""Functions used to calibrate the robot"""
import math

from robot import Robot
from robot.config import SPEED

bot = Robot(scale=1)


def main():
    """Start function"""
    bot.engage_pen()
    circle()
    bot.lift_pen()


def square(length=100):
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


def circle(radius=200):
    """Turns in a circle"""
    bot.drive_base.reset()
    bot.drive_base.drive(SPEED, math.degrees(SPEED / radius))
    while bot.drive_base.distance() < (2 * math.pi * radius):
        pass
    bot.drive_base.stop()


if __name__ == "__main__":
    main()
