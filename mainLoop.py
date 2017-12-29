#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
from stepperRobotArm import StepperRobotArm 
from replicaRobotArm import ReplicaRobotArm 
from button import Button
from switch import Switch

# - - - - - - - - - - - - - - - - 
# - - - - - GPIO Setup  - - - - -
# - - - - - - - - - - - - - - - -
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)  # Replay button
GPIO.setup(6, GPIO.IN)   # ON switch
GPIO.setup(13, GPIO.IN)  # Unused switch
GPIO.setup(19, GPIO.IN)  # Unused switch
GPIO.setup(26, GPIO.IN)  # Follow switch
GPIO.setup(12, GPIO.IN)  # Repeat switch
GPIO.setup(21, GPIO.OUT) # Replay LED

def lightOn():
    GPIO.output(21, 1)
def lightOff():
    GPIO.output(21, 0)

# - - - - - - - - - - - - - - - - 
# - - -  Global Objects - - - - -
# - - - - - - - - - - - - - - - -
stepperArm = StepperRobotArm()
replicaArm = ReplicaRobotArm()
replayButton = Button(20, stepperArm.shortPressAction, stepperArm.longPressAction)
onSwitch = Switch(6, lambda: True, lambda: True)
unused1Switch = Switch(13, lambda: True, lambda: True)
unused2Switch = Switch(19, lambda: True, lambda: True)
followSwitch = Switch(26, lambda: True, lambda: True)
repeatSwitch = Switch(12, lambda: True, lambda: True)

# - - - - - - - - - - - - - - - - 
# - - - - - MAIN LOOP - - - - - -
# - - - - - - - - - - - - - - - -
while True:
    # Update all switches / buttons
    replayButton.update()
    onSwitch.update()
    unused1Switch.update()
    unused2Switch.update()
    followSwitch.update()
    repeatSwitch.update()

    replicaArm.update()

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

