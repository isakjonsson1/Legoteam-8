import turtle
from robot.config import DRAWING_LEN


class Turtle:
    def __init__(self, update_freq=5):
        turtle.setworldcoordinates(0, 0, DRAWING_LEN, DRAWING_LEN)

        self.turtle = turtle.Turtle()
        self.screen = turtle.getscreen()
        self.distance_traveled = 0
        self.updates = 0
        self.update_freq = update_freq

    def drive(self, speed, turnrate):
        delta_pos = speed / 20
        delta_angle = turnrate / 20
        self.turtle.forward(delta_pos)
        self.turtle.left(delta_angle)

        self.distance_traveled += delta_pos

    def turn(self, angle):
        self.screen.update()
        self.screen.tracer(self.update_freq)
        self.turtle.left(angle)

    def straight(self, distance):
        self.screen.update()
        self.screen.tracer(self.update_freq)
        self.turtle.forward(distance)

    def distance(self):
        return self.distance_traveled

    def reset(self):
        self.distance_traveled = 0

    def pendown(self):
        self.turtle.pendown()

    def penup(self):
        self.turtle.penup()
