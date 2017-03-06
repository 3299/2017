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

    def guideSonic(self):
        difference = self.sonic.getCm('left') - self.sonic.getCm('right')
        average = (self.sonic.getCm('left') + self.sonic.getCm('right')) / 2

        difference = helpers.remap(difference, -40, 40, -1, 1)
        if (difference < -1):
            difference = -1
        elif (difference > 1):
            difference = 1

        powerX = 20 - average
        powerX = helpers.remap(powerX, -20, 60, -1, 1)

        print('PowerX: ' + str(powerX) + ', rotation: ' + str(difference))
        #self.chassis.cartesian(powerX, 0, difference)

        return

    def guideCamera(self, power):
        try:
            # contours
            centerX = self.sd.getNumberArray('x')
            centerY = self.sd.getNumberArray('y')
            areas   = self.sd.getNumberArray('areas')

            # camera viewport
            width = self.sd.getNumber('width')
            height = self.sd.getNumber('height')

            if (len(centerX) != 2 or len(centerY) != 2): # if only one strip can be seen (or more than two strips) don't do anything
                print('Cannot see two strips')
                return

            strafe = (((width - centerX[0]) - (width - centerX[1])) / 2 + centerX[0]) * 0.02 # center point of two targets relative to camera viewport, then scale down
            strafe = math.degrees(math.atan2(1, -strafe)) - 90
            power = ((areas[0] + areas[1]) / 2) * 0.0014

            # corrects so that robot is parallel with davit face
            rotate = self.sonic.getCm('right') - self.sonic.getCm('left')
            rotate = helpers.remap(rotate, -60, 60, 0, 360)

            #self.chassis.cartesian(power, strafe, rotate)
            #self.chassis.cartesian(0.5, 0, 0)

            print('Strafe: ' + str(strafe))
            print('Rotation: ' + str(rotate))
            print('Power: ' + str(power))

        except:
            print('error.vision: is the vision processing program running?')
            return
