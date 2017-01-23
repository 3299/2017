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
        self.driveTrain = wpilib.RobotDrive(Mapping.frontLeftM, Mapping.backLeftM, Mapping.frontRightM, Mapping.backRightM)
        self.driveTrain.setInvertedMotor(1, True)
        self.driveTrain.setInvertedMotor(2, True)
        self.driveTrain.setInvertedMotor(3, True)
        self.driveTrain.setExpiration(0.1)

        # Init other motors
        self.beltM      = wpilib.Talon(Mapping.beltM)

        # Init soleniods
        self.gearSol = {'in': wpilib.Solenoid(Mapping.gearSol['in']), 'out': wpilib.Solenoid(Mapping.gearSol['out'])}

        # Init joysticks
        self.leftJ      = wpilib.Joystick(Mapping.leftJ)
        self.middleJ    = wpilib.Joystick(Mapping.middleJ)
        self.rightJ     = wpilib.Joystick(Mapping.rightJ)

        # Init sensors
        self.gyroS      = wpilib.AnalogGyro(Mapping.gyroS)
        self.sonic      = wpilib.Ultrasonic(Mapping.sonicTrig, Mapping.sonicEcho)

        # Init LED strip
        self.ledStrip   = {'r': wpilib.PWM(Mapping.ledStrip['r']), 'g': wpilib.PWM(Mapping.ledStrip['g']), 'b': wpilib.PWM(Mapping.ledStrip['b'])}
