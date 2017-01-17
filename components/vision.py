"""
Communicates with the Raspberry Pi to get tracking info about the target. Usage:
vision = Vision()
print(vision.getData())
"""

import socket

class Vision(object):
    def __init__(self):
        # open socket
        try:
            self.sock = socket.socket()
            self.sock.connect(("10.32.99.73", 1182))
        except:
            return None

    def getData(self):
        # if socket has closed, except: will run
        try:
            self.sock.send(b'\r\n')
            data = self.sock.recv(256)
            data = data.decode("utf-8") # info comes back as a byte string
            data = data.strip() # remove any whitespace

            if (data.find(",") == -1): # no data
                return False
            else:
                data = data.split(',')

                i = 0
                for a in data:
                    if (i == 3):
                        a = a.replace(':','')

                    data[i] = float(a)
                    i = i + 1

                return data

        except: # re-opens the socket
            self.__init__()
            return self.getData()

    def getTurn(self):
        dataV = self.getData()
        if (dataV != False):
            print(str(dataV[1]) + ", ratio: " + str(dataV[3]))

            if (dataV[1] < 0):
                scale = -2.5
            else:
                scale = 2.5

            ratio = 1 - dataV[3] # optimally, the ratio would be 1, so we need to know how far away from 1 we are

            turn = dataV[1] * ratio * scale

            return turn
        else:
            return False
