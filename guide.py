"""
Guiding system for sonic sensor and vision.
"""

class Guiding(object):
    def __init__(self, sd, sonic, chassis):
        self.sd = sd
        self.sonic = sonic
        self.chassis = chassis

    def guideCamera(self, power):
        try:
            centerX = self.sd.getNumberArray('x')
            centerY = self.sd.getNumberArray('y')

            if (len(centerX) != 2 or len(centerY) != 2): # if only one strip can be seen don't do anything
                return
            
            width = self.sd.getNumber('w')
            height = self.sd.getNumber('h')

            strafe = ((width - centerX[0]) - (width - centerX[1])) / 2 + centerX[0]
            rotate = (centerY[1] - centerY[0])

            self.chassis.run(strafe * 0.6, 0, rotate * 4)
            print('Strafe: ' + str(strafe * 0.6))
            print('Rotation: ' + str(rotate * 4))

        except:
            return
