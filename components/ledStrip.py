"""
Outputs PWM values for controlling a RGB light strip.
"""
import math

class LedStrip(object):
    def __init__(self, pins):
        self.pins = pins
        self.blinkPeriod = 5 # x times per second

    def run(self, isRed, thirdColor, time):
        if (thirdColor == True):
            self.set({'r': True, 'g': True, 'b': True})
        else:
            if (isRed == True):
                self.set({'r': True, 'g': False, 'b': False})
            else:
                self.set({'r': False, 'g': False, 'b': True})

            if (time < 40):
                if (round(((time - math.floor(time)) * self.blinkPeriod) % 2) == 1):
                    self.set({'r': False, 'g': False, 'b': False})
                else:
                    if (isRed == True):
                        self.set({'r': True, 'g': False, 'b': False})
                    else:
                        self.set({'r': False, 'g': False, 'b': True})

    def set(self, output):
        self.pins['r'].set(output['r'])
        self.pins['g'].set(output['g'])
        self.pins['b'].set(output['b'])
