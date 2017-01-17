"""
Guiding system for sonic sensor and vision.
"""

class Guiding(object):
    def __init__(self, sd, sonic, chassis):
        self.sd = sd
        self.sonic = sonic
        self.chassis = chassis

    def guideCamera(self):
        centerX = self.sd.getNumberArray('x')
        centerY = self.sd.getNumberArray('y')
        print(centerX)
        #self.chassis.set(distance * 0.5, 0)
