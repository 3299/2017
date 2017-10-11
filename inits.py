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
        self.driveTrain = {'frontLeft': wpilib.Spark(Mapping.frontLeftM), 'backLeft': wpilib.Spark(Mapping.backLeftM), 'frontRight': wpilib.Spark(Mapping.frontRightM), 'backRight': wpilib.Spark(Mapping.backRightM)}
        self.driveTrain['frontLeft'].setInverted(True)
        self.driveTrain['backLeft'].setInverted(True)

        # Init other motors
        self.shooterM    = wpilib.Spark(Mapping.shooterM)
        self.hopperM     = wpilib.Spark(Mapping.hopperM)
        self.climbM      = wpilib.Spark(Mapping.climbM)
        self.groundGearM = wpilib.Talon(Mapping.groundGearM)

        # Init soleniods
        self.gearSol    = wpilib.DoubleSolenoid(Mapping.gearSol['out'], Mapping.gearSol['in'])
        self.groundSol  = wpilib.DoubleSolenoid(Mapping.groundGearSol['out'], Mapping.groundGearSol['in'])

        # Init sensors
        self.gyroS      = wpilib.ADXRS450_Gyro(Mapping.gyroS)
        self.allienceS  = wpilib.DigitalInput(Mapping.allienceS)
        self.shooterS   = wpilib.DigitalInput(Mapping.shooterS)
        self.hopperS    = wpilib.DigitalInput(Mapping.hopperS)

        # Init relays
        self.bumpPopR   = wpilib.Relay(Mapping.bumpPopR)
        self.greenLEDR  = wpilib.Relay(Mapping.greenLEDR)
