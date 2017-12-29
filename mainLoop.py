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
GPIO.setup(21, GPIO.OUT) 

def lightOn():
    GPIO.output(21, 1)
def lightOff():
    GPIO.output(21, 0)

# - - - - - - - - - - - - - - - - 
# - - -  Global Objects - - - - -
# - - - - - - - - - - - - - - - -
stepperArm = StepperRobotArm()
replicaArm = ReplicaRobotArm()
replayButton = Button(20, stepperArm.shortPressAction ,stepperArm.switchModes)

# - - - - - - - - - - - - - - - - 
# - - - - - MAIN LOOP - - - - - -
# - - - - - - - - - - - - - - - -
while True:
    replicaArm.update()
    replayButton.update()

    if stepperArm.checkIfIdle():
        if stepperArm.mode is 'follow':
            stepperArm.moveToPosition(replicaArm.posDict)
        if stepperArm.mode is 'replay':
            if stepperArm.replayStepList:
                reciever, command = stepperArm.replayStepList.pop(0)
                print(reciever, command)
                if reciever is 'arm':
                    stepperArm.moveToPositionRaw(command)

    time.sleep(0.1)

# let's think about that replay mode.
# let's do it differently:
# whenever we hit that longpress:
# chance mode:
