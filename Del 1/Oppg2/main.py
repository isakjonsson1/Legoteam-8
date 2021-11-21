#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
leftMotor = Motor(port=Port.A)
rightMotor = Motor(port=Port.B)
us = UltrasonicSensor(port=Port.S2)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=56, axle_track=82.1)
touchSensorOnOff = TouchSensor(port=Port.S1)
touchSensorAvslutt = TouchSensor(port=Port.S3)

""" 
To wait for the press of the on/off touch-sensor before executing the rest 
of the code, we can run the while-loop as long as the touch-sensor has not 
been pressed: 
"""

# As long as the on/off-button is not pressed, wait for it to be pressed 



def main():
    
    # while True:
    #     if touchSensorOnOff.pressed():
    #         kjør = not kjør
    #         while touchSensorOnOff.pressed():
    #             continue
    #     if kjør:
    #         if avstand() >= 50:
    #             drive(200,0)
    #         else:
    #             drive(-50)
    #             turn(30)

    
    while not touchSensorAvslutt.pressed():
        continue

    ev3.speaker.say("Exercise 2")
    kjør = True

    while not touchSensorAvslutt.pressed():
        if touchSensorOnOff.pressed():
            kjør = not kjør
            while touchSensorOnOff.pressed():
                if touchSensorAvslutt.pressed():
                    break
                continue 
        if kjør:
            robot.drive(-100,0)
            if avstand() <= 50:
                robot.stop()
                drive(-50)
                turn(20)
                robot.drive(-100,0)
        else:
            robot.stop()
    
    ev3.speaker.say("Exercise done")        
        
""" 
Since it is not allowed to have an empty loop, we use the 
`continue`-keyword. This keyword simply moves on to the next iteration of 
the while-loop. 
We could have just added a print statement to fill the loop, but this 
would fill up our terminal with unnecessary printing. 
"""

# Write your program here.

# avstand i mm
def drive(avstand):
    robot.straight(-avstand)

# vinkel er grader med klokka
def turn(vinkel):
    robot.turn(vinkel)

# avstand i mm
def avstand(): 
    distance = us.distance()
    return distance


main()