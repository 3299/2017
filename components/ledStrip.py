"""
Outputs PWM values for controlling a RGB light strip.
"""

class LedStrip(object):
    def __init__(self, pins):
        self.pins = pins

    def run(self, output):
        self.pins['r'].set(output['r'])
        self.pins['g'].set(output['g'])
        self.pins['b'].set(output['b'])
