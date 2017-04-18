"""
Inits wpilib objects
"""

import wpilib
from map import Map

class Component(object):
    def __init__(self):
        # Mapping object stores port numbers for all connected motors, sensors, and joysticks. See map.py.
        Mapping = Map()

        # Init drivetrain
        self.driveTrain = {'frontLeft': wpilib.Jaguar(Mapping.frontLeftM), 'backLeft': wpilib.Jaguar(Mapping.backLeftM), 'frontRight': wpilib.Jaguar(Mapping.frontRightM), 'backRight': wpilib.Jaguar(Mapping.backRightM)}
        self.driveTrain['frontLeft'].setInverted(True)
        self.driveTrain['backLeft'].setInverted(True)

        # Init other motors
        self.collectorM  = wpilib.Talon(Mapping.collectorM)
        self.shooterM    = wpilib.Talon(Mapping.shooterM)
        self.climbM      = wpilib.Talon(Mapping.climbM)
        self.groundGearM = wpilib.Talon(Mapping.groundGearM)

        # Init soleniods
        self.gearSol    = wpilib.DoubleSolenoid(Mapping.gearSol['out'], Mapping.gearSol['in'])
        self.groundSol  = wpilib.DoubleSolenoid(Mapping.groundGearSol['out'], Mapping.groundGearSol['in'])

        # Init joysticks
        self.leftJ      = wpilib.Joystick(Mapping.leftJ)
        self.middleJ    = wpilib.Joystick(Mapping.middleJ)
        self.rightJ     = wpilib.Joystick(Mapping.rightJ)

        # Init sensors
        self.gyroS      = wpilib.ADXRS450_Gyro(Mapping.gyroS)
        self.allienceS  = wpilib.DigitalInput(Mapping.allienceS)
        self.accelS     = wpilib.BuiltInAccelerometer()

        # Init Relay
        self.bumpPopR   = wpilib.Relay(Mapping.bumpPopR)

        # Init LED strip
        self.ledStrip   = {'r': wpilib.DigitalOutput(Mapping.ledStrip['r']), 'g': wpilib.DigitalOutput(Mapping.ledStrip['g']), 'b': wpilib.DigitalOutput(Mapping.ledStrip['b'])}
