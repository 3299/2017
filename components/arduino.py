"""
Facilitates communication between roboRIO and Arduino (for lights)
"""
class Arduino(object):
    def __init__(self, arduinoC):
        self.arduinoC = arduinoC

    def send(self, value):
        value = value.encode('ASCII')
        try:
            print(value)
            self.arduinoC.transaction(value, 0)
        except:
            pass
