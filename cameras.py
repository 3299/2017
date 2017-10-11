'''
Launches the camera streamers in a seperate
thread to prevent the main robot thread
from being overloaded.
'''

from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    usb1 = cs.startAutomaticCapture(dev=0)

    usb1.setResolution(320, 240)

    cs.waitForever()
