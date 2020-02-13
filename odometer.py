import struct, os

class odometer():
    def __init__(self):
        self.__file = open("/dev/input/mice", "rb");
        self.__x_ini = 0
        self.__y_ini = 0
        self.__x_fi = 0
        self.__y_fi = 0

    def start():
        buf = self.__file.read(3); 
        self.__x_ini,self.__y_ini = struct.unpack( "bb", buf[1:] )

    def stop():
        buf = self.__file.read(3)
        self.__x_fi,self.__y_fi = struct.unpack("bb", buf[1:] )
        x = self.__x_fi - self.__x_ini
        y = self.__y_fi - self.__y_ini
        return x, y