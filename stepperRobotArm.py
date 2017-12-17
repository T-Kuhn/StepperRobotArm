import time
from serial import Serial
import RPi.GPIO as GPIO

# - - - - - - - - - - - - - - - - 
# - - -  StepperRobotArm  - - - -
# - - - - - - - - - - - - - - - -
class StepperRobotArm:
    def __init__(self):
        self.port = Serial("/dev/ttyS0", baudrate=115200, timeout=0.001)
        self.wakeUpGrbl()
        self.useCurrentPosAsOrigin()
        self.currentPosDict = {"X": 0, "Y": 0, "Z": 0, "A": 0}

    def wakeUpGrbl(self):
        self.port.write(b"\r\n\r\n")
        print("waking up grbl")
        time.sleep(2)
        self.port.flushInput()

    def waitForResponse(self):
        self.port.readline()

    def sendBlock(self):
        port.write(b"G90 G0 X5.0 Y5.0 Z5.0 A1.0")
        port.write(b"\n")

    def sendTargetPositions(self, x, y, z, a):
        self.currentPosDict = {"X": x, "Y": y, "Z": z, "A": a}
        self.port.write(b"G90 G0 ")
        self.port.write(b" X" + "{:.4f}".format(x).encode())
        self.port.write(b" Y" + "{:.4f}".format(y).encode())
        self.port.write(b" Z" + "{:.4f}".format(z).encode())
        self.port.write(b" A" + "{:.4f}".format(a).encode())
        self.port.write(b"\n")
        self.waitForResponse()

    def getTotalChange(self, replicaArm):
        total = abs(-replicaArm.posDict["X"] - self.currentPosDict["X"])
        total = total + abs(replicaArm.posDict["Y"] - self.currentPosDict["Y"])
        total = total + abs(-replicaArm.posDict["Z"] - self.currentPosDict["Z"])
        total = total + abs(replicaArm.posDict["A"] - self.currentPosDict["A"])
        return total

    def useCurrentPosAsOrigin(self):
        self.port.write(b"G10 P0 L20 X0 Y0 Z0 A0")
        self.port.write(b"\n")
        self.waitForResponse()

# - - - - - - - - - - - - - - - - 
# - - - - - -  MEMO - - - - - - -
# - - - - - - - - - - - - - - - -
#port.write("{:.6f}".format(coordX))
