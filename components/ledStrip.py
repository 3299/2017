"""
Outputs PWM values for controlling a RGB light strip.
"""

class LedStrip(object):
    def __init__(self, pins):
        self.pins = pins

    def run(self, output):
        self.pins['r'].setRaw(int(output['r']))
        self.pins['g'].setRaw(int(output['g']))
        self.pins['b'].setRaw(int(output['b']))
