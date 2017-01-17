"""
Runs the belt.
"""

class Belt(object):
    def __init__(self, output):
        self.output = output

    def run(self, forward, backward):
        if (forward == True):
            self.output.set(-1)
        elif (backward == True):
            self.output.set(1)
        else:
            self.output.set(0)

    def set(self, value):
        self.output.set(value)
