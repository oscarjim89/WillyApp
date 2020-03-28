from time import sleep, time
from datetime import datetime
from gpiozero import Robot, InputDevice, OutputDevice
from picamera import PiCamera
from Storage import Repository
from desp2mongo import journalDB
from odometer import odometer
from math import sqrt, atan, degrees

class Willy(Robot):

    #Definicio constants
    MAX_SPEED = 0.293
    MAX_SEC_DEGREE = 2.25

    #Inicialitza
    def __init__(self, left, right, speed, sonar):
        self.__speed = speed
        self.__MxS = speed * self.MAX_SPEED
        self.__DxS = self.MAX_SEC_DEGREE / speed
        Robot.__init__(self, left, right)
        self.__trig = OutputDevice(sonar[0])
        self.__echo = InputDevice(sonar[1])
        self.__content = "/content"
        self.__record = 0 #Indica si hay un desplazamiento abierto
        self.__currMov = 0 #Movimiento en curso
        try:
            self.__odo = odometer()
        except:
            print ("Warning: Odometer (Mouse) no detectado!")
        try:
            self.__cam = PiCamera()
        except:
            print ("Warning: Camara no detectada!")    
        print("Hola! Estoy preparado!")

    #Mou cap a endavant la distancia en metres especificada
    def forward(self, distance):
        temps = distance / self.__MxS
        Robot.forward(self,self.__speed)
        sleep(temps)
        Robot.stop(self)        
        if (self.__record != 0):
            self.__record.updateJournal(distance,0)
        
    def rotatebyTime(self, direction, seconds):
        if (direction == 'left'):
            Robot.left(self,self.__speed)
        elif (direction == 'right'):
            Robot.right(self,self.__speed)
        else:
            print("Error: posibles valores: \"left\" o \"right\"")
        if seconds :
            sleep(seconds)
            Robot.stop(self)

    def rotatebyDegrees(self, degrees):
        if (degrees <= 180):
            temps = ( degrees * self.__DxS ) / 360
            Robot.right(self,self.__speed)
            sleep(temps)
            Robot.stop(self)
        else:
            degrees = 360 - degrees
            temps = ( degrees * self.__DxS ) / 360
            Robot.left(self,self.__speed)
            sleep(temps)
            Robot.stop(self)           

    #Mou cap a enrere la distancia en metres especificada
    def backward(self, distance):
        temps = distance / self.__MxS
        self.rotatebyDegrees(180)
        Robot.forward(self,self.__speed)
        sleep(temps)
        Robot.stop(self)
        if (self.__record != 0):
            self.__record.updateJournal(-distance,0)

    #Mou a la seva dreta la distancia en metres especificada
    def right(self, distance):
        temps = distance / self.__MxS
        self.rotatebyDegrees(90)
        Robot.forward(self,self.__speed)
        sleep(temps)
        Robot.stop(self)
        if (self.__record != 0):
            self.__record.updateJournal(0,distance)

    #Mou a la seva esquerra la distancia en metres especificada
    def left(self, distance):
        temps = distance / self.__MxS
        self.rotatebyDegrees(270)
        Robot.forward(self,self.__speed)
        sleep(temps)
        Robot.stop(self)
        if (self.__record != 0):
            self.__record.updateJournal(0,-distance)

    #Stop on click
    def stopClick(self):
        Robot.stop(self)
        if (self.__record != 0):
            try:
                x,y=self.__odo.stop()
                self.__record.updateJournal(x,y)
            except: 
                print("Warning: Odometer (Mouse) no detectado!")


    #Endavant on click
    def forwardClick(self):
        Robot.forward(self,self.__speed)
        if (self.__record != 0):
            try:
                self.__odo.start()
            except: 
                print("Warning: Odometer (Mouse) no detectado!")

    #Endarrere on click
    def backwardClick(self):
        self.rotatebyDegrees(180)
        Robot.forward(self,self.__speed)
        if (self.__record != 0):
            try:
                self.__odo.start()
            except: 
                print("Warning: Odometer (Mouse) no detectado!")

    #dreta on click
    def rightClick(self):
        self.rotatebyDegrees(90)
        Robot.forward(self,self.__speed)
        if (self.__record != 0):
            try:
                self.__odo.start()
            except: 
                print("Warning: Odometer (Mouse) no detectado!")


    #Esquerra on click
    def leftClick(self):
        self.rotatebyDegrees(270)
        Robot.forward(self,self.__speed)
        if (self.__record != 0):
            try:
                self.__odo.start()
            except: 
                print("Warning: Odometer (Mouse) no detectado!")


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

    #Algoritme dexploracio basic
    def Explora(self):
        while True:
            try:
                self.forwardClick()
                d = self.getSonar()

                if d < 20:
                    self.right(90)
            except KeyboardInterrupt:
                print("ya paro!")
                break

    #Retorna una foto
    def getPhoto(self):
        self.__cam.start_preview()
        sleep(3)
        now = datetime.today()
        f = self.__content+"capture_"+str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second)+".jpeg"
        try:
            self.__cam.capture(f)
        except:
            print("Error al echar la foto!")
            return
        self.__cam.stop_preview()

        return f

    def recordJournal(self,titol):
        try:
            self.__record = journalDB(titol)
        except:
            print("problemas al crear la BBDD")
            return 1
        return 0
    
    def goPosition(self,x,y):
        x = float(x)
        y = float(y)
 
        if (y == 0):
            if (x > 0):
                self.right(x)
            elif (x < 0):
                self.left(abs(x)) 
        elif (x == 0):
            if (y > 0):
                self.forward(y)
            elif (y < 0):
                self.backward(abs(y))
        else:
            h = sqrt((abs(x) * abs(x)) + (abs(y) * abs(y)))
            d = degrees(atan(abs(y) / abs(x)))

            if (x > 0) and (y > 0):
                self.rotatebyDegrees(d)
            elif (x < 0) and (y > 0):
                self.rotatebyDegrees(360-d)
            elif (x > 0) and (y < 0):
                self.rotatebyDegrees(90+d)
            elif (x < 0) and (y < 0):
                self.rotatebyDegrees(270-d)
            self.forward(round(h,1))


    #detecta si la imatge es interesant
    #def investiga(self,image):


#W = Willy(left=(17,18), right=(22,23), speed=0.5, sonar=(4,15))

#W.forward(2)
#W.right(90)
#W.forward(1)

#W.forwardClick()
#time.sleep(1)
#W.stop()
