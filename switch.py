#!/usr/bin/python3

import os
import time
import RPi.GPIO as GPIO

# - - - - - - - - - - - - - - - - 
# - - - -  SWITCH CLASS - - - - -
# - - - - - - - - - - - - - - - -
class Switch:
    def __init__(self, pin, switchOnFun, switchOffFun):
        self.pin = pin
        self.switchOnFun = switchOnFun
        self.switchOffFun = switchOffFun
        self.isOn = False 
        self.lastHighTime = 0
        self.SwitchOffTime = 100 # switch turns off after input was low for at least x ms

    def update(self):
        switchStatus = GPIO.input(self.pin)
        if switchStatus and not self.isOn:
            # Trigger on positive flank of Input Signal
            self.isOn = True
            self.switchOn()

        elif not switchStatus and self.isOn:
            # We get in here when the switch gets switched off
            if self.lastHighTime + self.SwitchOffTime < self.getTimeStamp():
                self.isOn = False
                self.switchOff()

        elif switchStatus and self.isOn:
            # Reset last hight Time
            self.lastHighTime = self.getTimeStamp()

    def getTimeStamp(self):
        # returns the current TimeStamp in millisecs
        return int(time.time()*1000)

    def switchOn(self):
        print("pin {0} ON".format(self.pin))
        self.switchOnFun()

    def switchOff(self):
        print("pin {0} OFF".format(self.pin))
        self.switchOffFun()
