import time
from gpiozero import Robot

class Willy(Robot):
   
    #Definicio constants
    MAX_SPEED = 0.45
    MAX_SEC_DEGREE = 1.15

    #Inicialitza 
    def __init__(self, left, right, speed):
        
        self.__speed = speed
        self.__MxS = speed * self.MAX_SPEED
        Robot.__init__(self, left, right)

    #Mou cap a endavant la distancia en metres especificada
    def forward(self, distancia):
        
        temps = distancia / self.__MxS
        
        Robot.forward(self,self.__speed)
        time.sleep(temps)
        Robot.stop(self)

    #Mou cap a enrere la distancia en metres especificada
    def backward(self, distance):
        
        temps = distance / self.__MxS

        Robot.backward(self,self.__speed)
        time.sleep(temps)
        Robot.stop(self)

    #Gira cap a la dreta els graus especificats
    def right(self, degrees):
    
        temps = ( degrees * self.MAX_SEC_DEGREE ) / 360
        Robot.right(self)
        time.sleep(temps)
        Robot.stop(self)

    #Gira cap a la esquerra els graus especificats
    def left(self, degrees):

        temps = ( degrees * self.MAX_SEC_DEGREE ) / 360
        Robot.left(self)
        time.sleep(temps)
        Robot.stop(self)

#W = Willy(left=(17,18), right=(22,23), speed=1)

#W.forward(0.5)
#W.right(180)
#W.backward(0.5)
