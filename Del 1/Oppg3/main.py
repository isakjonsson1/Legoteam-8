#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random 
import time

#Oppgaven:
#-roboten skal kjøre på en bane (15 mm bred svart strek ) 
#-roboten skal kjøre mot klokka
#-hvert 10. sekund skal roboten stoppe og underholde publikum
#-mot slutten dukker det opp en hindring på banen. Roboten skal stoppe 5-20cm fra denne hindringen og spille av enten lyden “CHEERING” eller “FANFARE”.
#ev3.speaker.play_file(SoundFile.CHEERING)

#Om underholdning:
#-må implementere minst 4 forskjellige underholdningsbidrag (hva som helst)
#-for hvert stopp skal nummeret velges TILFELDIG 


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
leftMotor = Motor(port=Port.A)
rightMotor = Motor(port=Port.B)
us = UltrasonicSensor(port=Port.S3)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=56, axle_track=82.1)
leftColorSensor = ColorSensor(port=Port.S1)
rightColorSensor = ColorSensor(port=Port.S2)


# Global variables that defines the maximum RGB-values a sensor-reading 
# from the color-sensor can have for the color to be defined as black 
# RED = ​50 
# GREEN = ​50 
# BLUE = ​50 
 
# Get the percentage of red, green, and blue color from the color-sensor 
# (red, green, blue) = colorSensor.rgb() 
# If any of the colors from the sensor has lower rgb-values than what we 
# defined in our global variables, then the color is assumed to be black 
# is_black = red < RED ​or ​green < GREEN ​or​ blue < BLUE 

# Write your program here.
def main():
    global RED, GREEN, BLUE
    RED, GREEN, BLUE = leftColorSensor.rgb()
    RED /= 2
    GREEN /= 2
    BLUE /= 2

    t0 = time.time()
    turnrate = 0
    while us.distance() > 100:
        robot.drive(-80, turnrate)
        t1 = time.time()

        if t1 - t0 > 10:
            robot.stop()
            entertainment()
            t0 = time.time()
            
        if isBlack(rightColorSensor):
            turnrate = -100
        elif isBlack(leftColorSensor):
            turnrate = 100
        else:
            turnrate = 0

    robot.stop()
    ev3.speaker.play_file(SoundFile.CHEERING)


def isBlack(colorSensor):
    global RED, GREEN, BLUE

    red, green, blue = colorSensor.rgb()

    return (red < RED and green < GREEN and blue < BLUE)

def entertainment():
    random_integer = random.randint(1,5)
    if random_integer == 1:
        ev3.speaker.play_file(SoundFile.ELEPHANT_CALL)
    elif random_integer == 2:
        ev3.speaker.say("VIL DU HØRE EN VITS?")
        wait(1000)
        ev3.speaker.say("KATTA MED SLIPPS!")
        wait(1000)
        ev3.speaker.say("VIL DU HØRE RESTEN?!")
        wait(1000)
        ev3.speaker.say("ROMPA TIL PRESTEN!!")
        ev3.speaker.say("HA. HA. HA.")
        ev3.speaker.play_file(SoundFile.LAUGHING_1)
    elif random_integer == 3:
        drive(20)
        drive(-20)
        drive(20)
        drive(-20)  
        ev3.speaker.play_file(SoundFile.DOG_BARK_2)
    elif random_integer == 4:
        robot.turn(60)
        robot.turn(-60)
        robot.turn(60)
        robot.turn(-60)
        ev3.speaker.play_file(SoundFile.CAT_PURR)

def turn(vinkel):
    robot.turn(vinkel)
    
def drive(avstand):
    robot.straight(-avstand)

# avstand i mm
def avstand(): 
    distance = us.distance()
    return distance

if __name__ == "__main__":
    main()