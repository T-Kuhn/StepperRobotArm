#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
from threading import Thread

"""
A class for controlling a servo via pigpio deamon
This class should get updated in it's own thread.
"""
# - - - - - - - - - - - - - - - - 
# - - - SERVO GRIPPER CLASS - - -
# - - - - - - - - - - - - - - - -
class ServoGripper:
    def __init__(self, pigpiod_pi, servoPin):
        self.pi = pigpiod_pi
        self.servoPin = servoPin
        self.targetPos = 0
        self.currentPos = 0
        self.mode = 'idle'
        self.sleepTime = 0.001
        # available modes are:
        # - idle
        # - moving
        self.startUpdateThread()

    def startUpdateThread(self):
        self.t = Thread(target=self.update, args=())
        self.t.start()

    def setTargetPos(self, targetPos):
        self.targetPos = targetPos

    def update(self):
        while True:
            self.updateCurrentPos()
            self.pi.set_servo_pulsewidth(self.servoPin, 1000 + self.currentPos)
            time.sleep(self.sleepTime)

    def updateCurrentPos(self):
        if self.targetPos > self.currentPos:
            self.mode = "moving"
            self.currentPos += 1
        elif self.targetPos < self.currentPos:
            self.mode = "moving"
            self.currentPos -= 1
        else:
            self.mode = "idle"
