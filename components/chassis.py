"""
Drives. Can accept input from joysticks or values [-1, 1].
Uses the wheel-attached encoders as input for a threaded PID
loop on each wheel.
"""
import helpers
import wpilib
import math

from networktables import NetworkTable

class encoderRemaped(object):
    def __init__(self, encoder, reversed):
        self.encoder = encoder
        self.reversed = reversed

    def pidGet(self):
        if (self.reversed == True):
            return helpers.remap(self.encoder.getRate(), -130, 130, 1, -1)
        else:
            return helpers.remap(self.encoder.getRate(), -130, 130, -1, 1)

    def getPIDSourceType(self):
        return 1

class Chassis(object):
    def __init__(self, drive, encoders, gyro):
        self.drive     = drive
        self.encoders  = encoders
        self.gyro      = gyro
        self.jDeadband = 0.05
        self.sd = NetworkTable.getTable('SmartDashboard')

        # reset all encoders when code restarts
        self.encoders['frontLeft'].reset()
        self.encoders['frontRight'].reset()
        self.encoders['backLeft'].reset()
        self.encoders['backRight'].reset()

        # remap encoders before plugging them into PID
        self.encoders['frontLeftR'] =  encoderRemaped(self.encoders['frontLeft'], False)
        self.encoders['frontRightR'] = encoderRemaped(self.encoders['frontRight'], False)
        self.encoders['backLeftR'] =   encoderRemaped(self.encoders['backLeft'], True)
        self.encoders['backRightR'] =  encoderRemaped(self.encoders['backRight'], False)

        # PID values
        self.pids      = {'p': 0.8, 'i': 0.6, 'd': 0.02}

        # Tune PID on Smart Dashboard
        self.sd.putNumber('p', self.pids['p'])
        self.sd.putNumber('i', self.pids['i'])
        self.sd.putNumber('d', self.pids['d'])

        # Init PID loops
        self.pidLoops  = {'frontLeft': wpilib.PIDController(self.pids['p'], self.pids['i'], self.pids['d'], self.encoders['frontLeftR'], self.drive['frontLeft']),
                          'backLeft': wpilib.PIDController(self.pids['p'], self.pids['i'], self.pids['d'], self.encoders['backLeftR'], self.drive['backLeft']),
                          'frontRight': wpilib.PIDController(self.pids['p'], self.pids['i'], self.pids['d'], self.encoders['frontRightR'], self.drive['frontRight']),
                          'backRight': wpilib.PIDController(self.pids['p'], self.pids['i'], self.pids['d'], self.encoders['backRightR'], self.drive['backRight'])}
        self.pidLoops['frontLeft'].enable()
        self.pidLoops['backLeft'].enable()
        self.pidLoops['frontRight'].enable()
        self.pidLoops['backRight'].enable()

        self.pidLoops['frontLeft'].setContinuous(True)
        self.pidLoops['frontRight'].setContinuous(True)
        self.pidLoops['backLeft'].setContinuous(True)
        self.pidLoops['backRight'].setContinuous(True)

    def run(self, leftX, leftY, rightX, rightY, microLeft, microTop, microRight, microBackward, reverse, drivingMethod):
        '''
        print('Front left: ', round(self.encoders['frontLeft'].getRate(), 0),
              'Front right: ', round(self.encoders['frontRight'].getRate(), 0),
              'Back left: ', round(self.encoders['backLeft'].getRate(), 0),
              'Back right: ', round(self.encoders['backRight'].getRate(), 0))
        '''

        if (drivingMethod == 'bobcat'):
            if (reverse == True):
                multiplier = -1
            else:
                multiplier = 1

                self.bobcat(
                    helpers.raiseKeepSign(leftX, 2) * multiplier + 0.5*(microRight - microLeft),
                    helpers.raiseKeepSign(leftY, 2) * multiplier + 0.5*(microBackward - microTop),
                    helpers.raiseKeepSign(rightX, 2) * multiplier + 0.5*(microRight - microLeft),
                    helpers.raiseKeepSign(rightY, 2) * multiplier + 0.5*(microBackward - microTop))

        elif (drivingMethod == 'arcade'):
            self.arcade(leftX, leftY, rightX, rightY)

    def bobcat(self, x1, y1, x2, y2):
        powerY = (y1 + y2) / 2 # average of Y axis for going forward/backward
        powerX = (x1 + x2) / 2 # average of X axis for strafing
        rotate = (y1 - y2) / 2

        if (-0.4 < rotate < 0.4):
            rotate = 0

        self.cartesian(powerX, powerY, rotate * 0.75)

    def arcade(self, x1, y1, x2, y2):
        direction = math.degrees(math.atan2(x2, -y2))

        self.polar(abs(y1), direction, x1)

    def cartesian(self, x, y, rotation):
        p = self.sd.getNumber('p')
        i = self.sd.getNumber('i')
        d = self.sd.getNumber('d')
        self.pidLoops['frontLeft'].setPID(p, i, d)
        self.pidLoops['frontRight'].setPID(p, i, d)
        self.pidLoops['backLeft'].setPID(p, i, d)
        self.pidLoops['backRight'].setPID(p, i, d)

        frontLeft = -x + y + rotation
        frontRight = x + y - rotation
        backLeft = x + y + rotation
        backRight = -x + y - rotation

        self.pidLoops['frontLeft'].setSetpoint(frontLeft)
        self.pidLoops['frontRight'].setSetpoint(frontRight)
        self.pidLoops['backLeft'].setSetpoint(backLeft)
        self.pidLoops['backRight'].setSetpoint(backRight)

    def polar(self, power, direction, rotation):
        power = power * math.sqrt(2.0)
        # The rollers are at 45 degree angles.
        dirInRad = math.radians(direction + 45)
        cosD = math.cos(dirInRad)
        sinD = math.sin(dirInRad)

        speeds = [0] * 4
        speeds[0] = sinD * power + rotation
        speeds[1] = cosD * power - rotation
        speeds[2] = cosD * power + rotation
        speeds[3] = sinD * power - rotation

        # Normalize values - make sure they are all -1 < x < 1
        maxMagnitude = max(abs(x) for x in speeds)
        if maxMagnitude > 1.0:
            for i in range(len(speeds)):
                speeds[i] = speeds[i] / maxMagnitude

        print('Front left: ', speeds[0])
        print('Front right: ', speeds[1])
        print('Back left: ', speeds[2])
        print('Back right: ', speeds[3])

        self.pidLoops['frontLeft'].setSetpoint(speeds[0])
        self.pidLoops['frontRight'].setSetpoint(speeds[1])
        self.pidLoops['backLeft'].setSetpoint(speeds[2])
        self.pidLoops['backRight'].setSetpoint(speeds[3])
