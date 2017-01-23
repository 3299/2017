"""
Drives. Can accept input from joysticks or values [-1, 1]. Uses the gyro for better steering.
"""
import math
import helpers

class Chassis(object):
    def __init__(self, drive, gyro):
        self.drive = drive
        self.gyro  = gyro

        self.Kp    = 0.03

    def run(self, leftX, leftY, rightX):
        self.drive.mecanumDrive_Cartesian(leftX, leftY, rightX, self.gyro.getAngle())

    def arcadeDrive(self, x, y):
        self.drive.arcadeDrive(x, y)

    def set(self, power, direction, rotation):
        self.drive.mecanumDrive_Polar(power, direction, rotation)
