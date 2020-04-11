import struct, os
import threading
from time import sleep

class odometer():

    def __init__(self):

        self.__MOUSE_TO_CM = 405.7
        self.__file = open("/dev/input/mice", "rb")
        self.__x = 0
        self.__y = 0
        self.__buf = 0
        self.__terminate = False
        self.__t = threading.Thread(target=self.activate, daemon=True)

        self.__t.start()

    def activate(self):
        while not self.__terminate:
            self.__buf = self.__file.read(3)
            dis_x,dis_y = struct.unpack( "bb", self.__buf[1:] )
            self.__x = self.__x + (dis_x / self.__MOUSE_TO_CM)
            self.__y = self.__y + (dis_y / self.__MOUSE_TO_CM)
    
    def reset(self):
        self.__x = 0
        self.__y = 0
        self.__terminate = True
        sleep(2)
        self.__terminate = False
        self.__t = threading.Thread(target=self.activate, daemon=True)
        self.__t.start()

    def getOdo(self):
        return self.__x, self.__y