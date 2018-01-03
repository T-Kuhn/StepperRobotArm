#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
from stepperRobotArm import StepperRobotArm 
from replicaRobotArm import ReplicaRobotArm 
from blinkLED import BlinkLED 
from button import Button
from switch import Switch
import pigpio

# - - - - - - - - - - - - - - - - 
# - - - - - GPIO Setup  - - - - -
# - - - - - - - - - - - - - - - -
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)  # Replay button
GPIO.setup(16,GPIO.IN)   # Delete button 
GPIO.setup(6, GPIO.IN)   # ON switch
GPIO.setup(13, GPIO.IN)  # Unused switch
GPIO.setup(19, GPIO.IN)  # Unused switch
GPIO.setup(26, GPIO.IN)  # Follow switch
GPIO.setup(12, GPIO.IN)  # Repeat switch
GPIO.setup(21, GPIO.OUT) # Blink LED
servoGripperPin = 24     # Servo Gripper

# - - - - - - - - - - - - - - - - 
# - - -  Global Objects - - - - -
# - - - - - - - - - - - - - - - -
pi = pigpio.pi('localhost', 8888)

blinkLED = BlinkLED(21)
stepperArm = StepperRobotArm(blinkLED, pi, servoGripperPin)
replicaArm = ReplicaRobotArm()

replayButton = Button(20, stepperArm.shortPressAction, lambda: True)
deleteButton = Button(16, stepperArm.deleteReplayList, lambda: True)

onSwitch = Switch(6, lambda: True, lambda: True)
endlessRepeatSwitch = Switch(13, lambda: stepperArm.setEndlessReplay(True), lambda: stepperArm.setEndlessReplay(False))
setOriginSwitch = Switch(19, replicaArm.getCorrValues, lambda: True)
followSwitch = Switch(26, lambda: stepperArm.setMode('follow'), lambda: stepperArm.setMode('idle'))
repeatSwitch = Switch(12, lambda: stepperArm.setMode('replay'), lambda: stepperArm.setMode('idle'))

# - - - - - - - - - - - - - - - - 
# - - - UPDATE INPUT DEVICES  - -
# - - - - - - - - - - - - - - - -
def updateInputDevices():
    replayButton.update()
    deleteButton.update()
    onSwitch.update()
    endlessRepeatSwitch.update()
    setOriginSwitch.update()
    followSwitch.update()
    repeatSwitch.update()

# - - - - - - - - - - - - - - - - 
# - -  UPDATE OUTPUT DEVICES  - -
# - - - - - - - - - - - - - - - -
def updateOutputDevices():
    blinkLED.update()

# - - - - - - - - - - - - - - - - 
# - - - - UPDATE ROBOT ARM  - - -
# - - - - - - - - - - - - - - - -
def updateRobotArm():
    if stepperArm.mode is 'follow':
        if stepperArm.checkIfIdle():
            stepperArm.moveToPosition(replicaArm.posDict)
        # TODO: add check whether servo is idle or not.
        stepperArm.moveGripperToPosition(replicaArm.servoPos)
    elif stepperArm.mode is 'replay':
        if stepperArm.checkIfIdle():
            if stepperArm.replayStepList:
                blinkLED.setMode('slowBlink')
                reciever, command = stepperArm.replayStepList.pop(0)
                print(reciever, command)
                if reciever is 'arm':
                    stepperArm.moveToPositionRaw(command)
                if reciever is 'gripper':
                    stepperArm.moveGripperToPosition(command)
            else:
                blinkLED.setMode('idle')
                stepperArm.replayEnded()

# - - - - - - - - - - - - - - - - 
# - - - - - MAIN LOOP - - - - - -
# - - - - - - - - - - - - - - - -
while True:
    updateInputDevices()
    updateOutputDevices()
    replicaArm.update()
    updateRobotArm()
    time.sleep(0.1)
