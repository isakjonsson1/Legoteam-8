"""File that holds the Robot class"""
import math

from pybricks.parameters import Stop

from app.point import Point
from app.curves import Line
from robot.config import drive_base, pen_motor, TURN_SPEED, TURN_RATE, PEN_TORQUE, SPEED


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
        # True if drivebase is Turtle
        self.turtle = not isinstance(_drive_base, type(drive_base))
        self.pen_motor = _pen_motor
        self.pen_state = False

    def lift_pen(self):
        """Lifts the pen from the paper"""
        if self.turtle:
            self.drive_base.penup()
            return

        if self.pen_state:
            self.pen_motor.run_angle(TURN_SPEED, TURN_RATE, then=Stop.HOLD, wait=True)

        self.pen_state = False

    def engage_pen(self):
        """Puts the pen on the paper"""
        if self.turtle:
            self.drive_base.pendown()
            return

        if not self.pen_state:
            self.pen_motor.run_until_stalled(
                TURN_SPEED, then=Stop.COAST, duty_limit=PEN_TORQUE
            )

        self.pen_state = True

    def calibrate_pen(self):
        """Used to calibrate the pen and test functionality"""
        self.engage_pen()
        self.lift_pen()
        self.pen_state = False

    def drive_through_path(self, path, drawing=True):
        """Drives through a given path"""
        for curve in path:
            self.drive_through_curve(curve, drawing=drawing)

    def drive_through_curve(self, curve, drawing=True):
        """
        Drives the robot to the start position of the curve and drives through it.
        """
        self.lift_pen()
        # Moves the robot
        self.move_to(curve.get_start_pos())
        self.change_angle(curve.get_start_angle())

        if drawing:
            self.engage_pen()

        # Follows the curve
        self.drive_base.reset()
        while (
            self.drive_base.distance() is None and curve.length() != 0
        ) or self.drive_base.distance() < curve.length() * self.scale:

            distance = self.drive_base.distance()
            if distance is None:
                distance = 0

            try:
                t_param = curve.get_t(distance / self.scale)
            except ValueError:
                break

            curvature = curve.get_curvature(t_param)
            self.drive_base.drive(SPEED, math.degrees(SPEED * curvature / self.scale))

        # Updates params
        self.angle = curve.get_end_angle()
        self.pos = curve.get_end_pos()

    def move_to(self, pos):
        """Moves to a specified point in the coordinates system of the curves."""
        # Defines the length
        line = Line([self.pos, pos])

        # No change if line length is zero
        if line.length() > 1e-5:
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
        angle_delta = ((end_angle - self.angle) + math.pi) % (math.pi * 2) - math.pi
        self.drive_base.turn(math.degrees(angle_delta))

        # Update params
        self.angle = end_angle
