"""Holds the Turtle class"""
import turtle
from robot.config import DRAWING_LEN


class Turtle:
    """The turtle object is used to simulate a ev3 drivebase's movement"""

    def __init__(self, sampling_freq=250, update_freq=10):
        """Initiates a new Turtle instance.

        sampling_freq is how many times per simulated second the position is updated.
        update_freq is how many position updates it takes before the image is refreshed
        """

        self.turtle = turtle.Turtle()
        self.screen = turtle.Screen()

        self.screen.setworldcoordinates(0, 0, DRAWING_LEN, DRAWING_LEN)
        self.distance_traveled = 0
        self.updates = 0
        self.update_freq = update_freq
        self.sampling_freq = sampling_freq

    def drive(self, speed, turnrate):
        """Drives one step with the given speed and turnrate."""
        delta_pos = speed / self.sampling_freq
        delta_angle = turnrate / self.sampling_freq
        self.turtle.forward(delta_pos)
        self.turtle.left(delta_angle)

        self.distance_traveled += delta_pos

    def turn(self, angle):
        """Turns the to the left the amount (in deg) given."""
        self.screen.update()
        self.screen.tracer(self.update_freq)
        self.turtle.left(angle)

    def straight(self, distance):
        """Drives straight for the distane given."""
        self.screen.update()
        self.screen.tracer(self.update_freq)
        self.turtle.forward(distance)

    def distance(self):
        """Retuns the driven distance since last self.reset"""
        return self.distance_traveled

    def stop(self):
        """Stops the turtle (dosnt't actually do anything)"""
        return

    def reset(self):
        """Resets the driven distance."""
        self.distance_traveled = 0

    def pendown(self):
        """The path driven now paints a line"""
        self.turtle.pendown()

    def penup(self):
        """The path driven now does not paint a line"""
        self.turtle.penup()
