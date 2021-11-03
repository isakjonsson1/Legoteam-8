"""File that holds the Robot class"""
import math

from pybricks.parameters import Stop

from app.point import Point
from app.curves import Line
from robot.config import drive_base, pen_motor, SPEED


class Robot:
    """
    Keeps track of where the robot is and what angle it is rotated.

    Provides useful methods to move the robot around and to draw control the pen.
    """

    def __init__(
        self,
        scale,
        start_angle=0,
        start_pos=Point(x=0, y=0),
        _drive_base=drive_base,
        _pen_motor=pen_motor,
    ):
        """
        Creates a new robot instance.

        Scale is the factor used to convert from the coordinates of the curves
        to the coordinates of the real world.

        drive_base is the DriveBase instance of the robot.

        pen_motor is the motor that drives the pen.
        """
        self.scale = scale
        self.angle = start_angle
        self.pos = start_pos
        self.drive_base = _drive_base
        self.pen_motor = _pen_motor

    def lift_pen(self):
        """Lifts the pen from the paper"""
        self.pen_motor.run_target(360, 270, then=Stop.HOLD, wait=True)

    def engage_pen(self):
        """Puts the pen on the paper"""
        self.pen_motor.run_target(-360, 0, then=Stop.HOLD, wait=True)

    def drive_through_path(self, path):
        """Drives through a given path"""
        for curve in path:
            self.drive_through_curve(curve)

    def drive_through_curve(self, curve):
        """
        Drives the robot to the start position of the curve and drives through it.
        """
        # Moves the robot
        self.move_to(curve.get_start_pos())
        self.change_angle(curve.get_start_angle())

        # Follows the curve
        self.drive_base.reset()
        while self.drive_base.distance() < curve.length() * self.scale:
            t_param = curve.get_t(self.drive_base.distance)
            curve = curve.get_curvature(t_param)
            self.drive_base.drive(SPEED, math.degrees(SPEED * curve / self.scale))

        # Updates params
        self.angle = curve.get_end_angle()
        self.pos = curve.get_end_pos()

    def move_to(self, pos):
        """Moves to a specified point in the coordinates system of the curves."""
        # Defines the length
        line = Line([self.pos, pos])

        # No change if line length is zero
        if line.length() < 1e-5:
            # Changes angle
            self.change_angle(line.get_start_angle())

            # Drives the line
            self.drive_base.straight(line.length() * self.scale)

            # Updates params
            self.angle = line.get_end_angle()
            self.pos = line.get_end_pos()

    def change_angle(self, end_angle):
        """
        Turns the robot in the direction specified by the end_angle (in radians).
        """
        angle_delta = (((end_angle - self.angle) + math.pi) % math.tau) - math.pi
        self.drive_base.turn(math.degrees(angle_delta))

        # Update params
        self.angle = end_angle
