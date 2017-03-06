"""
Helper class for ultrasonic sensor
"""
import statistics
import wpilib

class Sonic(object):
    def __init__(self, sensor):
        self.sensor = sensor
        self.lastMeasurement = {'left': 0, 'right': 0}
        self.lastSensor = 'left'
        self.sensorOn = False
        self.timer = wpilib.Timer()
        self.lastTime = 0
        self.period = 200

    def run(self):
        if ((self.timer.getMsClock() - self.lastTime) > self.period):
            if (self.sensorOn == False):
                if (self.lastSensor == 'left'):
                    self.sensor['rightR'].pulse(255)
                if (self.lastSensor == 'right'):
                    self.sensor['leftR'].pulse(255)
                self.sensorOn = True
            else:
                if (self.lastSensor == 'left'):
                    averageVoltage = self.sensor['rightS'].getAverageVoltage()
                    distance = (averageVoltage * 1000)/4.9
                    self.sensor['rightR'].pulse(0)
                    self.lastMeasurement['right'] = distance
                    self.lastSensor = 'right'
                if (self.lastSensor == 'right'):
                    averageVoltage = self.sensor['leftS'].getAverageVoltage()
                    distance = (averageVoltage * 1000)/4.9
                    self.sensor['leftR'].pulse(0)
                    self.lastMeasurement['left'] = distance
                    self.lastSensor = 'left'

                self.sensorOn = False

            self.lastTime = self.timer.getMsClock()


    def getCm(self, side):
        return self.lastMeasurement[side]
