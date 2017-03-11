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
        #self.driveTrain.setInvertedMotor(1, True)
        self.driveTrain['frontLeft'].setInverted(True)
        #self.driveTrain.setInvertedMotor(3, True)
        self.driveTrain['backLeft'].setInverted(True)
        #self.driveTrain.setExpiration(0.1)

        # Init other motors
        self.collectorM  = wpilib.Talon(Mapping.collectorM)
        self.shooterM    = wpilib.Talon(Mapping.shooterM)
        self.climbM      = wpilib.Talon(Mapping.climbM)

        # Init servos
        self.ballServos = {'servo1': wpilib.Servo(Mapping.servo1), 'servo2': wpilib.Servo(Mapping.servo2)}

        # Init soleniods
        self.gearSol    = wpilib.DoubleSolenoid(Mapping.gearSol['out'], Mapping.gearSol['in'])

        # Init joysticks
        self.leftJ      = wpilib.Joystick(Mapping.leftJ)
        self.middleJ    = wpilib.Joystick(Mapping.middleJ)
        self.rightJ     = wpilib.Joystick(Mapping.rightJ)

        # Init sensors
        self.gyroS      = wpilib.AnalogGyro(Mapping.gyroS)
        self.allienceS  = wpilib.DigitalInput(Mapping.allienceS)

        # Init encoders
        self.encoders   = {'frontLeft':  wpilib.Encoder(Mapping.encoders['frontLeft'][0], Mapping.encoders['frontLeft'][1], True),
                           'frontRight': wpilib.Encoder(Mapping.encoders['frontRight'][0], Mapping.encoders['frontRight'][1], True),
                           'backLeft':   wpilib.Encoder(Mapping.encoders['backLeft'][0], Mapping.encoders['backLeft'][1], True),
                           'backRight':  wpilib.Encoder(Mapping.encoders['backRight'][0], Mapping.encoders['backRight'][1], True)}
        self.encoders['frontLeft'].setDistancePerPulse(0.073)
        self.encoders['frontRight'].setDistancePerPulse(0.073)
        self.encoders['backLeft'].setDistancePerPulse(0.073)
        self.encoders['backRight'].setDistancePerPulse(0.073)

        self.encoders['frontLeft'].pidSource = 1

        # Init Relay
        self.bumpPopR   = wpilib.DigitalOutput(Mapping.bumpPopR)

        # Init LED strip
        self.ledStrip   = {'r': wpilib.DigitalOutput(Mapping.ledStrip['r']), 'g': wpilib.DigitalOutput(Mapping.ledStrip['g']), 'b': wpilib.DigitalOutput(Mapping.ledStrip['b'])}
