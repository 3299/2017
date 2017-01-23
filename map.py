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
        self.frontLeftM  = 2
        self.frontRightM = 1
        self.backLeftM   = 0
        self.backRightM  = 3

        self.beltM       = 9

        # Soleniods
        self.gearSol = {'in': 0, 'out': 2}

        # Sensors have suffix 'S'. Gyro and sonar use analog in, everything else uses the DIO.
        self.gyroS       = 0
        self.sonicTrig   = 2
        self.sonicEcho   = 3

        # LED strip
        self.ledStrip    = {'r': 4, 'g': 5, 'b': 6}

        pass
