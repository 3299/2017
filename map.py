"""
Defines port numbers for motors and sensors.
"""

class Map(object):
    def __init__(self):
        # Joysticks have suffix 'J'
        self.leftJ       = 0
        self.middleJ     = 1
        self.rightJ      = 2

        # Motors have suffix 'M'. All motors use PWM.
        self.frontLeftM  = 0
        self.frontRightM = 1
        self.backLeftM   = 2
        self.backRightM  = 3

        self.climbM      = 4

        self.collectorM  = 5
        self.shooterM    = 6

        # Servos are also plugged into the PWM slots.
        self.servo1      = 7
        self.servo2      = 15

        # Soleniods
        self.gearSol     = {'in': 2, 'out': 0}

        # Sensors have suffix 'S'. Gyro uses analog in, everything else uses the DIO.
        self.gyroS       = 0
        self.allienceS   = 16

        # Encoders are plugged into the custom passive expansion board for the roboRio's MXP port.
        self.encoders    = {'frontLeft': [4, 5], 'frontRight': [2, 3], 'backLeft': [0, 1], 'backRight': [6, 7]}

        # Relay
        self.bumpPopR    = 0

        # LED strip (connected to DIO).
        self.ledStrip    = {'r': 10, 'g': 11, 'b': 9}
