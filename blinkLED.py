#!/usr/bin/python3

import os
import time
import RPi.GPIO as GPIO

"""
A class for the use of a LED ouput on Raspberry Pi.
This class provides:
- blinking functionality 
"""
# - - - - - - - - - - - - - - - - 
# - - - - BLINK LED CLASS - - - -
# - - - - - - - - - - - - - - - -
class BlinkLED:
    def __init__(self, pin):
        self.pin = pin
        self.blinkCounter = 0
        self.updateCounter = 0
        self.slowBlinkSwitchCount = 5
        self.fastBlinkSwitchCount = 2
        self.LEDIsOn = False
        GPIO.output(self.pin, 0)
        self.mode = 'idle'
        # available modes are:
        # - idle
        # - fastBlinkTwice
        # - slowBlink

    def setMode(self, mode):
        self.resetUpdateCounter()
        if mode is 'fastBlinkTwice':
            self.mode = 'fastBlinkTwice'
        elif mode is 'slowBlink':
            self.mode = 'slowBlink'
        elif mode is 'idle':
            self.mode = 'idle'
        else:
            raise NameError('unknown mode.')

    def update(self):
        self.updateCounter += 1
        if self.mode is 'idle':
            GPIO.output(self.pin, 0)
            self.LEDIsOn = False
        elif self.mode is 'slowBlink':
            self.slowBlink()
        elif self.mode is 'fastBlinkTwice':
            self.fastBlinkTwice()

    def fastBlinkTwice(self):
        if self.updateCounter >= self.fastBlinkSwitchCount:
            self.resetUpdateCounter()
            self.switchOutput()
            self.blinkCounter += 1
            if self.blinkCounter >= 3:
                self.setMode('idle')
                self.resetBlinkCounter()

    def slowBlink(self):
        if self.updateCounter >= self.slowBlinkSwitchCount:
            self.resetUpdateCounter()
            self.switchOutput()

    def switchOutput(self):
        if self.LEDIsOn:
            GPIO.output(self.pin, 0)
            self.LEDIsOn = False
        else:
            GPIO.output(self.pin, 1)
            self.LEDIsOn = True 

    def resetUpdateCounter(self):
        self.updateCounter = 0

    def resetBlinkCounter(self):
        self.blinkCounter = 0
