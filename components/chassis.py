"""
Drives. Can accept input from joysticks or values [-1, 1]. Uses the gyro for better steering.
"""
import helpers
import wpilib

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

        self.pids      = {'p': 0.8, 'i': 0.6, 'd': 0.02}

        self.sd.putNumber('p', self.pids['p'])
        self.sd.putNumber('i', self.pids['i'])
        self.sd.putNumber('d', self.pids['d'])

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

    def run(self, leftX, leftY, rightX, rightY, squared, reverse):
        powerY = (leftY + rightY) / 2 # average of Y axis for going forward/backward
        powerX = (leftX + rightX) / 2 # average of X axis for strafing
        rotate = (leftY - rightY) / -2

        if (squared == True):
            if (powerY < 0):
                powerY = powerY**2
                powerY = powerY * -1
            else:
                powerY = powerY**2
            if (powerX < 0):
                powerX = powerX**2
                powerX = powerX * -1
            else:
                powerX = powerX**2
            if (rotate < 0):
                rotate = rotate**2
                rotate = rotate * -1
            else:
                rotate = rotate**2

            powerY = helpers.curve(powerY)
            powerX = helpers.curve(powerX)
        else:
            # deadband on rotate 20% only when not squarring inputs
            if (rotate < 0.2 and rotate > -0.2):
                rotate = 0
            if (powerX < 0.2 and powerX > -0.2):
                powerX = 0

        if (reverse == True):
            powerY = - powerY
            powerX = - powerX

        self.cartesian(-powerX, powerY, -rotate * 0.75)

    def set(self, power, direction, rotation):
        self.drive.mecanumDrive_Polar(power, direction, rotation)

    def cartesian(self, x, y, rotation):
        p = self.sd.getNumber('p')
        i = self.sd.getNumber('i')
        d = self.sd.getNumber('d')
        self.pidLoops['frontLeft'].setPID(p, i, d)
        self.pidLoops['frontRight'].setPID(p, i, d)
        self.pidLoops['backLeft'].setPID(p, i, d)
        self.pidLoops['backRight'].setPID(p, i, d)

        frontLeft = x + y + rotation
        frontRight = -x + y - rotation
        backLeft = -x + y + rotation
        backRight = x + y - rotation

        self.pidLoops['frontLeft'].setSetpoint(frontLeft)
        self.pidLoops['frontRight'].setSetpoint(frontRight)
        self.pidLoops['backLeft'].setSetpoint(backLeft)
        self.pidLoops['backRight'].setSetpoint(backRight)
