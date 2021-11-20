"""Configuration file"""
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase


# Motors and drive base
pen_motor = Motor(port=Port.D, positive_direction=Direction.CLOCKWISE)
left_motor = Motor(port=Port.A)
right_motor = Motor(port=Port.B)
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=128)

# ev3
ev3 = EV3Brick()

# Constants
SPEED = 50
DRAWING_LEN = 600

# pen_motor
TURN_SPEED = 100
TURN_RATE = 300

# Torque in percent
PEN_TORQUE = 35
