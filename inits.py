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
        self.driveTrain = wpilib.RobotDrive(wpilib.Spark(Mapping.frontLeftM), wpilib.Spark(Mapping.backLeftM), wpilib.Spark(Mapping.frontRightM), wpilib.Spark(Mapping.backRightM))
        self.driveTrain.setInvertedMotor(1, True)
        self.driveTrain.setInvertedMotor(3, True)
        self.driveTrain.setExpiration(0.1)

        # Init other motors
        self.collectorM      = wpilib.Jaguar(Mapping.collectorM)

        # Init soleniods
        self.gearSol    = wpilib.DoubleSolenoid(Mapping.gearSol['out'], Mapping.gearSol['in'])

        # Init joysticks
        self.leftJ      = wpilib.Joystick(Mapping.leftJ)
        self.middleJ    = wpilib.Joystick(Mapping.middleJ)
        self.rightJ     = wpilib.Joystick(Mapping.rightJ)

        # Init sensors
        self.gyroS      = wpilib.AnalogGyro(Mapping.gyroS)
        self.sonicS     = {'leftS': wpilib.AnalogInput(Mapping.sonicS['left']), 'leftR': wpilib.DigitalOutput(Mapping.sonicS['left']), 'rightS': wpilib.AnalogInput(Mapping.sonicS['right']), 'rightR': wpilib.DigitalOutput(Mapping.sonicS['right'])}

        # Init LED strip
        self.ledStrip   = {'r': wpilib.PWM(Mapping.ledStrip['r']), 'g': wpilib.PWM(Mapping.ledStrip['g']), 'b': wpilib.PWM(Mapping.ledStrip['b'])}
