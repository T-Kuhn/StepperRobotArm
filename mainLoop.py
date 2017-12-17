#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
from stepperRobotArm import StepperRobotArm 
from replicaRobotArm import ReplicaRobotArm 
from button import Button

# - - - - - - - - - - - - - - - - 
# - - - - - GPIO Setup  - - - - -
# - - - - - - - - - - - - - - - -
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN) 
#GPIO.setup(21, GPIO.OUT) 

# - - - - - - - - - - - - - - - - 
# - - -  Global Objects - - - - -
# - - - - - - - - - - - - - - - -
stepperArm = StepperRobotArm()
replicaArm = ReplicaRobotArm()
button = Button()

# - - - - - - - - - - - - - - - - 
# - - - - - MAIN LOOP - - - - - -
# - - - - - - - - - - - - - - - -
while True:
    replicaArm.update()
    button.update(GPIO.input(20))

    if stepperArm.checkIfIdle():
        stepperArm.moveToPosition(replicaArm.posDict)

    
    time.sleep(0.2)
