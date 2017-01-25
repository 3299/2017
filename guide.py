"""
Guiding system for sonic sensor and vision.
"""

import helpers
import math

class Guiding(object):
    def __init__(self, sd, sonic, chassis):
        self.sd = sd
        self.sonic = sonic
        self.chassis = chassis

    def guideCamera(self, power):
        try:
            centerX = self.sd.getNumberArray('x')
            centerY = self.sd.getNumberArray('y')
            areas   = self.sd.getNumberArray('areas')

            if (len(centerX) != 2 or len(centerY) != 2): # if only one strip can be seen don't do anything
                print('Cannot see two strips')
                return

            width = self.sd.getNumber('width')
            height = self.sd.getNumber('height')

            strafe = (((width - centerX[0]) - (width - centerX[1])) / 2 + centerX[0]) * 0.02
            strafe = math.degrees(math.atan2(1, -strafe)) - 90
            power = ((areas[0] + areas[1]) / 2) * 0.0014

            rotate = (areas[1] - areas[0])

            rotate = helpers.remap(rotate, -(width * height) / 10, (width * height) / 10, -1, 1)


            #self.chassis.set(power, strafe, rotate)
            print('Strafe: ' + str(strafe))
            print('Rotation: ' + str(rotate))
            print('Power: ' + str(power))

        except:
            return
