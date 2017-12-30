#!/usr/bin/python3

import os
import time
import RPi.GPIO as GPIO

"""
A class for the use of pushbuttons connected to the Raspberry Pi.
Buttons need to be pulled down (via external pull down resistor or 
by using the pull down functionality of the microcontroller). 
This class provides:
- software debounce (no chattering)
- execution of different functions on short press / long press
"""
# - - - - - - - - - - - - - - - - 
# - - - -  BUTTON CLASS - - - - -
# - - - - - - - - - - - - - - - -
class Button:
    def __init__(self, pin, shortPressFun, longPressFun):
        self.pin = pin
        self.pressedFlag = False 
        self.helperFlag1 = False 
        self.releasedCounter = 0
        self.longPressTime = 1000;      # All time related properties in millisecs 
        self.pressStartTime = 0;
        self.pressEndTime = 0;
        self.pressDuration = 0
        self.shortPressFun = shortPressFun
        self.longPressFun = longPressFun

    def update(self):
        buttonStatus = GPIO.input(self.pin)
        if buttonStatus and not self.helperFlag1:
            # Trigger on positive flank of Button Input Signal
            self.pressedFlag = True;
            self.helperFlag1 = True
            self.pressStartTime = self.getTimeStamp()
            # helperFlag1 needs to be resetted after the Buttonpress was registered correctly
        elif not buttonStatus and self.pressedFlag:
            # We get in here when the button was pressed but isn't pressed anymore
            self.releasedCounter += 1;
            if self.releasedCounter >= 2:
                self.pressedFlag = False
                self.helperFlag1 = False
                self.releasedCounter = 0
                self.pressEndTime = self.getTimeStamp()
                self.pressDuration = self.pressEndTime - self.pressStartTime
                if self.pressDuration >= self.longPressTime:
                    # Long Press!
                    self.longPress()
                else:
                    # Short Press!
                    self.shortPress()
        elif buttonStatus and self.pressedFlag:
            # Reset the releasedCounter if the buttonStatus gets high again very fast
            self.releasedCounter = 0;

    def getTimeStamp(self):
        # returns the current TimeStamp in millisecs
        return int(time.time()*1000)

    def longPress(self):
        print("pin {0} long press".format(self.pin))
        self.longPressFun()

    def shortPress(self):
        print("pin {0} short press".format(self.pin))
        self.shortPressFun()
