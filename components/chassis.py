"""
Drives. Can accept input from joysticks or values [-1, 1]. Uses the gyro for better steering.
"""
import math
import helpers

class Chassis(object):
    def __init__(self, drive, gyro):
        self.drive = drive
        self.gyro  = gyro

    def run(self, leftX, leftY, rightX, rightY):
        #self.drive.mecanumDrive_Cartesian(leftY, leftX, rightX, 0)
        powerY = (leftY + rightY) / 2 # average of Y axis for going forward/backward
        powerX = (leftX + rightX) / 2 # average of X axis for strafing
        rotate = (leftY - rightY) / 2

        self.drive.mecanumDrive_Cartesian(powerX, powerY, rotate, 0)

    def arcadeDrive(self, x, y):
        self.drive.arcadeDrive(x, y)

    def set(self, power, direction, rotation):
        self.drive.mecanumDrive_Polar(power, direction, rotation)
