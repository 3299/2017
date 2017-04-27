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
        self.collectorM  = wpilib.Talon(Mapping.collectorM)
        self.shooterM    = wpilib.Spark(Mapping.shooterM)
        self.climbM      = wpilib.Spark(Mapping.climbM)
        self.groundGearM = wpilib.Spark(Mapping.groundGearM)

        # Init soleniods
        self.gearSol    = wpilib.DoubleSolenoid(Mapping.gearSol['out'], Mapping.gearSol['in'])
        self.groundSol  = wpilib.DoubleSolenoid(Mapping.groundGearSol['out'], Mapping.groundGearSol['in'])

        # Init joystick
        self.joystick   = wpilib.XboxController(0)

        # Init sensors
        self.gyroS      = wpilib.ADXRS450_Gyro(Mapping.gyroS)
        self.allienceS  = wpilib.DigitalInput(Mapping.allienceS)
        self.accelS     = wpilib.BuiltInAccelerometer()

        # Init relays
        self.bumpPopR   = wpilib.Relay(Mapping.bumpPopR)
        self.greenLEDR  = wpilib.Relay(Mapping.greenLEDR)
