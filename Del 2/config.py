"""Configuration file"""
from pybricks.ev3devices import Motor
from pybricks.ev3devices import TouchSensor
from pybricks.ev3devices import ColorSensor

# from pybricks.ev3devices import InfraredSensor
# from pybricks.ev3devices import UltrasonicSensor
# from pybricks.ev3devices import GyroSensor

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

# Motors and drive base
left_motor = Motor(port=Port.A)
right_motor = Motor(port=Port.B)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=82.1)

# Sensors
button = TouchSensor(port=Port.S3)
back_color_sensor = ColorSensor(port=Port.S2)
front_color_sensor = ColorSensor(port=Port.S1)

ev3 = EV3Brick()
