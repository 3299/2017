"""
Drives. Can accept input from joysticks or values [-1, 1].
Uses the wheel-attached encoders as input for a threaded PID
loop on each wheel.
"""
import helpers
import wpilib
import math

from networktables import NetworkTable

class Chassis(object):
    def __init__(self, drive, gyro):
        self.drive     = drive
        self.gyro      = gyro
        self.jDeadband = 0.05
        self.sd = NetworkTable.getTable('SmartDashboard')

    def run(self, leftX, leftY, rightX, rightY, microLeft, microTop, microRight, microBackward, reverse, drivingMethod):
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
            self.arcade(helpers.raiseKeepSign(leftX, 2) + 0.4*(microRight - microLeft),
                        helpers.raiseKeepSign(leftY, 2) + 0.4*(microBackward - microTop),
                        rightX, rightY)

    def bobcat(self, x1, y1, x2, y2):
        powerY = (y1 + y2) / 2 # average of Y axis for going forward/backward
        powerX = (x1 + x2) / 2 # average of X axis for strafing
        rotate = (y1 - y2) / 2

        if (-0.4 < rotate < 0.4):
            rotate = 0

        self.cartesian(powerX, powerY, rotate * 0.75)

    def arcade(self, x1, y1, x2, y2):
        # rotation deadzone
        if (-0.10 < x2 < 0.10):
            rotation = 0
        else:
            rotation = helpers.raiseKeepSign(-x2, 2) * 0.75

        direction = math.degrees(math.atan2(-x1, y1))

        # deadzone on power
        if (-0.1 < (abs(x1) + abs(y1))/2 < 0.1):
            power = 0
        else:
            if (abs(x1) > abs(y1)):
                power = abs(x1)
            elif (abs(x1) < abs(y1)):
                power = abs(y1)
            else:
                power = 1

        self.polar(power, direction, rotation)

    def cartesian(self, x, y, rotation):
        frontLeft = -x + y + rotation
        frontRight = x + y - rotation
        backLeft = x + y + rotation
        backRight = -x + y - rotation

        self.drive['frontLeft'].set(frontLeft)
        self.drive['frontRight'].set(frontRight)
        self.drive['backLeft'].set(backLeft)
        self.drive['backRight'].set(backRight)

    def polar(self, power, direction, rotation):
        if (power == 'last'):
            power = self.lastPower
        else:
            self.lastPower = power

        if (direction == 'last'):
            direction = self.lastDirection
        else:
            self.lastDirection = direction

        if (rotation == 'last'):
            rotation = self.lastRotation
        else:
            self.lastRotation = rotation

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

        self.drive['frontLeft'].set(speeds[0])
        self.drive['frontRight'].set(speeds[1])
        self.drive['backLeft'].set(speeds[2])
        self.drive['backRight'].set(speeds[3])

    def speedsToDirection(self, frontLeft, frontRight, backLeft, backRight):
    	x = (backLeft - frontLeft) / 2
    	y = (frontLeft + frontRight) / 2
    	rotation = (backLeft - frontRight) / 2

    	direction = math.degrees(math.atan2(x, -y))

    	return {'direction': -direction, 'rotation': rotation}
