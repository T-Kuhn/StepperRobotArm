#!/usr/bin/python3

import time
from serial import Serial

# - - - - - - - - - - - - - - - - 
# - - -  StepperRobotArm  - - - -
# - - - - - - - - - - - - - - - -
class StepperRobotArm:
    def __init__(self, led):
        self.blinkLED = led
        self.port = Serial("/dev/ttyS0", baudrate=115200, timeout=0.001)
        self.wakeUpGrbl()
        self.useCurrentPosAsOrigin()
        self.currentPosDict = {"X": 0, "Y": 0, "Z": 0, "A": 0}
        self.replayList = []
        self.replayStepList = []
        self.mode = 'idle'
        self.endlessReplay = False
        # available modes are:
        # - idle
        # - follow
        # - replay

    def wakeUpGrbl(self):
        self.port.write(b"\r\n\r\n")
        print("waking up grbl")
        time.sleep(2)
        self.port.flushInput()

    def waitForResponse(self):
        return self.port.readline()

    def sendBlock(self):
        port.write(b"G90 G0 X5.0 Y5.0 Z5.0 A1.0")
        port.write(b"\n")

    def checkIfIdle(self):
        self.port.write(b"?")
        if b"Idle" in self.waitForResponse():
            return True
        else:
            return False

    def setMode(self, mode):
        if mode is 'follow':
            self.mode = 'follow'
        elif mode is 'replay':
            self.mode = 'replay'
        elif mode is 'idle':
            self.mode = 'idel'
        else:
            raise NameError('unknown mode.')

    def moveToPosition(self, targetPosDict):
        self.sendTargetPositions(
            -targetPosDict["X"], 
            targetPosDict["Y"], 
            -targetPosDict["Z"], 
            targetPosDict["A"])

    def moveToPositionRaw(self, targetPosDict):
        self.sendTargetPositions(
            targetPosDict["X"], 
            targetPosDict["Y"], 
            targetPosDict["Z"], 
            targetPosDict["A"])

    def sendTargetPositions(self, x, y, z, a):
        self.currentPosDict = {"X": x, "Y": y, "Z": z, "A": a}
        self.port.write(b"G90 G0 ")
        self.port.write(b" X" + "{:.4f}".format(x).encode())
        self.port.write(b" Y" + "{:.4f}".format(y).encode())
        self.port.write(b" Z" + "{:.4f}".format(z).encode())
        self.port.write(b" A" + "{:.4f}".format(a).encode())
        self.port.write(b"\n")
        self.waitForResponse()

    def getTotalChange(self, rArmPosDict):
        total = abs(-rArmPosDict["X"] - self.currentPosDict["X"])
        total = total + abs(rArmPosDict["Y"] - self.currentPosDict["Y"])
        total = total + abs(-rArmPosDict["Z"] - self.currentPosDict["Z"])
        total = total + abs(rArmPosDict["A"] - self.currentPosDict["A"])
        return total

    def shortPressAction(self):
        # This function gets executed on short button press.
        if self.mode is 'follow':
            self.saveCurrentPos()
        else:
            self.prepareReplay()

    def saveCurrentPos(self):
        print("saving current pos")
        self.replayList.append(('arm', dict(self.currentPosDict)))
        self.blinkLED.setMode('fastBlinkTwice')

    def prepareReplay(self):
        # copy replay list into replay step list
        self.replayStepList = list(self.replayList)

    def deleteReplayList(self):
        print("Deleting replayList.")
        self.replayList = []

    def setEndlessReplay(self, value):
        print('endless replay:', value)
        self.endlessReplay = value 

    def replayEnded(self):
        if self.endlessReplay:
            self.prepareReplay()

    def useCurrentPosAsOrigin(self):
        self.port.write(b"G10 P0 L20 X0 Y0 Z0 A0")
        self.port.write(b"\n")
        self.waitForResponse()
