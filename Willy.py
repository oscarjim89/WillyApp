from time import sleep, time
from gpiozero import Robot, InputDevice, OutputDevice

class Willy(Robot):

    #Definicio constants
    MAX_SPEED = 0.45
    MAX_SEC_DEGREE = 1.15

    #Inicialitza
    def __init__(self, left, right, speed, sonar):
        self.__speed = speed
        self.__MxS = speed * self.MAX_SPEED
        self.__DxS = self.MAX_SEC_DEGREE / speed
        Robot.__init__(self, left, right)
        self.__trig = OutputDevice(sonar[0])
        self.__echo = InputDevice(sonar[1])
        print("Hola! Estoy preparado!")

    #Mou cap a endavant la distancia en metres especificada
    def forward(self, distance):
        temps = distance / self.__MxS

        Robot.forward(self,self.__speed)
        sleep(temps)
        Robot.stop(self)

    #Mou cap a enrere la distancia en metres especificada
    def backward(self, distance):
        temps = distance / self.__MxS

        Robot.backward(self,self.__speed)
        sleep(temps)
        Robot.stop(self)

    #Gira cap a la dreta els graus especificats
    def right(self, degrees):
        temps = ( degrees * self.__DxS ) / 360

        Robot.right(self,self.__speed)
        sleep(temps)
        Robot.stop(self)

    #Gira cap a la esquerra els graus especificats
    def left(self, degrees):
        temps = ( degrees * self.__DxS ) / 360

        Robot.left(self,self.__speed)
        sleep(temps)
        Robot.stop(self)

    #Stop on click
    def stopClick(self):
        Robot.stop(self)

    #Endavant on click
    def forwardClick(self):
        Robot.forward(self,self.__speed)

    #Endarrere on click
    def backwardClick(self):
        Robot.backward(self,self.__speed)

    #dreta on click
    def rightClick(self):
        Robot.right(self,self.__speed)

    #Esquerra on click
    def leftClick(self):
        Robot.left(self,self.__speed)

    #Printa per pantalla la distancia en cm
    def getSonar(self):
        self.__trig.on()
        sleep(0.00001)
        self.__trig.off()

        while self.__echo.is_active == False:
            pulse_start = time()
        while self.__echo.is_active == True:
            pulse_end = time()

        sleep(0.06)
        duration = pulse_end - pulse_start
        speed = 343
        distance = (speed * duration / 2) * 100
        #print(str(round(distance,1)) + "cm")
        return distance



W = Willy(left=(17,18), right=(22,23), speed=0.5, sonar=(4,15))

while True:
    try:
        W.forwardClick()
        d = W.getSonar()
    
        if d < 20:
            W.right(90)
    except KeyboardInterrupt:
        print "ya paro!"
        break
#W.forward(2)
#W.right(90)
#W.forward(1)

#W.forwardClick()
#time.sleep(1)
#W.stop()
