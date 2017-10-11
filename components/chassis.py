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
        self.drive          = drive
        self.gyro           = gyro
        self.jDeadband      = 0.05
        self.pidAngle       = wpilib.PIDController(0.4, 0, 0.1, self.anglePIDInput, output=self.anglePIDOutput)

        self.pidAngle.setInputRange(-180.0, 180.0)
        self.pidAngle.setOutputRange(-1.0, 1.0)
        self.pidAngle.setAbsoluteTolerance(1)
        self.pidAngle.setContinuous(False)
        self.pidRotateRate = 0

    def run(self, leftX, leftY, rightX, microLeft, microTop, microRight, microBackward):
        self.arcade(helpers.raiseKeepSign(leftX, 2) + 0.4*(microRight - microLeft),
                    helpers.raiseKeepSign(leftY, 2) + 0.4*(microBackward - microTop),
                    rightX)

    def arcade(self, x1, y1, x2):
        # rotation curve
        rotation = helpers.raiseKeepSign(-x2, 2) * 0.75
        self.cartesian(x1, y1, rotation)

    def cartesian(self, x, y, rotation):
        speeds = [0] * 4

        speeds[0] = -x + y + rotation
        speeds[1] = x + y - rotation
        speeds[2] = x + y + rotation
        speeds[3] = -x + y - rotation

        if (max(speeds) > 1):
            maxSpeed = max(speeds)
            for i in range (0, 4):
                speeds[i] = maxSpeed / speeds[i]

        self.drive['frontLeft'].set(speeds[0])
        self.drive['frontRight'].set(speeds[1])
        self.drive['backLeft'].set(speeds[2])
        self.drive['backRight'].set(speeds[3])

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

        self.drive['frontLeft'].set(speeds[0])
        self.drive['frontRight'].set(speeds[1])
        self.drive['backLeft'].set(speeds[2])
        self.drive['backRight'].set(speeds[3])

    def driveToAngle(self, power, angle, continuous):
        self.gyro.reset()
        self.pidAngle.setSetpoint(angle)
        self.pidAngle.enable()
        self.pidAngle.setContinuous(continuous)

        if (continuous == True): # if true, runs continuously (for driving straight)
            print(self.pidRotateRate)
            self.cartesian(0, -power, -self.pidRotateRate)
        else:
            while (abs(self.pidAngle.getError()) > 2):
                print(self.pidAngle.getError())
                self.cartesian(0, 0, -self.pidRotateRate)

            self.pidAngle.disable()
            self.cartesian(0, 0, 0)
            self.gyro.reset()
            return;

    def anglePIDInput(self):
        return self.gyro.getAngle()

    def anglePIDOutput(self, value):
        self.pidRotateRate = value

    def speedsToDirection(self, frontLeft, frontRight, backLeft, backRight):
    	x = (backLeft - frontLeft) / 2
    	y = (frontLeft + frontRight) / 2
    	rotation = (backLeft - frontRight) / 2

    	direction = math.degrees(math.atan2(x, -y))

    	return {'direction': -direction, 'rotation': rotation}
