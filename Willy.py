from time import sleep, time
from datetime import datetime
from gpiozero import Robot, InputDevice, OutputDevice
from picamera import PiCamera
from Storage import Repository
from desp2mongo import journalDB
from odometer import odometer
from math import sqrt, atan, degrees

class Willy(Robot):

    #Constants definition
    MAX_SPEED = 0.293 #Calibration parameter: Distance in 1 meter
    MAX_SEC_DEGREE = 2.25 #Calibration parameter: Seconds in 360 degrees
    ROT_SPEED = 0.5 #Velocitat de rotació pel gir calibrat: robot.right/.left (motiu: modificació speedL i speedR)

    #Init Willy object
    #Example: Willy(left=(17,18), right=(22,23), speed=0.5, sonar=(4,15))
    def __init__(self, left, right, speed_left, speed_right, sonar):
        self.__speedL = speed_left #Global speed intensity (float [0..1]).
        self.__speedR = speed_right #Global speed intensity (float [0..1]).
        self.__MxS = self.ROT_SPEED * self.MAX_SPEED #Normalize constants with intensity
        self.__DxS = self.MAX_SEC_DEGREE / self.ROT_SPEED #Normalize constants with intensity
        Robot.__init__(self, left, right) #Robot object declaration
        self.__trig = OutputDevice(sonar[0]) #Set sonar output Pin
        self.__echo = InputDevice(sonar[1]) #Set sonar input Pin
        self.__content = "/content" #Local folder to save content
        self.__record = 0 #Indicates if the moves have to be recorded
        self.__currmov = 0 #indicates that are a movement in active.

        #Try to run the mouse odometer
        try:
            self.__odo = odometer()
        except:
            print ("Warning: Odometer (Mouse) not detected!")
        
        #Try to run de Pi Camera
        try:
            self.__cam = PiCamera()
        except:
            print ("Warning: Camera not detected!")    

        print("Hi! I am ready!")

    #Moves forward the input distance (input in meters)
    def forward(self, distance):
        temps = distance / self.__MxS
        Robot.forward(self,self.__speedL,self.__speedR)
        sleep(temps)
        Robot.stop(self)
        
    #Rotate by time in the specified direction
    def rotatebyTime(self, direction, seconds):
        if (direction == 'left'):
            Robot.left(self,self.ROT_SPEED)
        elif (direction == 'right'):
            Robot.right(self,self.ROT_SPEED)
        else:
            print("Error: posibles valores: \"left\" o \"right\"")
        if seconds :
            sleep(seconds)
            Robot.stop(self)

    def rotatebyDegrees(self, degrees):
        if (degrees <= 180):
            temps = ( degrees * self.__DxS ) / 360
            Robot.right(self,self.ROT_SPEED)
            sleep(temps)
            Robot.stop(self)
        else:
            degrees = 360 - degrees
            temps = ( degrees * self.__DxS ) / 360
            Robot.left(self,self.ROT_SPEED)
            sleep(temps)
            Robot.stop(self)           

    #Mou cap a enrere la distancia en metres especificada
    def backward(self, distance):
        temps = distance / self.__MxS
        self.rotatebyDegrees(180)
        Robot.forward(self,self.__speedL,self.__speedR)
        sleep(temps)
        Robot.stop(self)

    #Mou a la seva dreta la distancia en metres especificada
    def right(self, distance):
        temps = distance / self.__MxS
        self.rotatebyDegrees(90)
        Robot.forward(self,self.__speedL,self.__speedR)
        sleep(temps)
        Robot.stop(self)

    #Mou a la seva esquerra la distancia en metres especificada
    def left(self, distance):
        temps = distance / self.__MxS
        self.rotatebyDegrees(270)
        Robot.forward(self,self.__speedL,self.__speedR)
        sleep(temps)
        Robot.stop(self)

    #Stop on click
    def stopClick(self):
        Robot.stop(self)
        if (self.__record != 0):
            try:
                x,y=self.__odo.getOdo()
                self.__record.updateJournal(x,y)
            except:
                print("Warning: Problems updating odometer position..")

    #Endavant on click
    def forwardClick(self):
        if (self.__record != 0):
            x,y=self.__odo.getOdo()
            print(x,y)
            self.__record.updateJournal(x,y)            
        Robot.forward(self,self.__speedL,self.__speedR)

    #Endarrere on click
    def backwardClick(self):
        if (self.__record != 0):
            try:
                x,y=self.__odo.getOdo()
                self.__record.updateJournal(x,y)
            except:
                print("Warning: Problems updating odometer position..")
        self.rotatebyDegrees(180)
        Robot.forward(self,self.__speedL,self.__speedR)

    #dreta on click
    def rightClick(self):
        if (self.__record != 0):
            try:
                x,y=self.__odo.getOdo()
                self.__record.updateJournal(x,y)
            except:
                print("Warning: Problems updating odometer position..")
        self.rotatebyDegrees(90)
        Robot.forward(self,self.__speedL,self.__speedR)

    #Esquerra on click
    def leftClick(self):
        if (self.__record != 0):
            try:
                x,y=self.__odo.getOdo()
                self.__record.updateJournal(x,y)
            except:
                print("Warning: Problems updating odometer position..")
        self.rotatebyDegrees(270)
        Robot.forward(self,self.__speedL,self.__speedR)

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

    #Inicia la grabación dun nou desplacament
    def recordJournal(self,titol):
        try:
            self.__record = journalDB(titol)
            res = self.__record.getJournalid()
        except:
            print("problemas al crear la BBDD")
            return 1
        if (res == None):
            return 2
        return 0
    
    #Es desplaca segons coordinades x,y
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

        if (self.__record != 0):
            self.__record.updateJournal(x,y)

    def isRecording(self):
        return self.__record

    #Corrige el desplazamiento de la X/Y para que siempre sea el especificado en fix.
    #La función será ejecutada por un thread en paralelo que se iniciará cuando se ejecute un desplazamiento de tipo XXXClick()
    #Se puede utilizar la variable global self.__currmov que después se pueda parar el thread.
    #Entrada:
    #  fix: valor en cm que se ha de mantener fijo
    #  axis: eje a fijar. posibles valores: [x,y]
    #Salida:
    #  No retorna nada.

    #AHORA SOLO APLICA FORWARD SIMPLE:
    def forward_v2(self):
        vel_base = 0.5
        p=0
        p_ant=0
        i=0
        d=0
        kp=10
        ki=0.5
        kd=1

        self.__currmov=1
        Robot.forward(self.__speedL,self.__speedR)

        while (self.__currmov):
            xo,yo=self.__odo.getOdo()
            p=0-xo #-3.5
            i=i+p #-9.5
            d=p-p_ant #-7.5
            p_ant=p #-3.5
            if ((p*i)<0):
                 i=0
            errorPID= (kp*p + ki*i + kd*d)/10 #-0.16
            if (errorPID>0.5):
                errorPID=0.5
            elif (errorPID<-0.5):
                errorPID=-0.5

            #TODO: Asegurar-se de que el rang del errorPID sigui abs(0.5)
            if(errorPID>abs(0.15)):
                Robot.forward(vel_base+errorPID,vel_base-errorPID)

    '''
    #p_amb_el_sinus:
    xo,yo=self.__odo.getOdo()
    #TODO:treure xf i yf del GoTo.
    sin=(yo-yf)/sqrt((xf-xo)^2+(yf-yo)^2)'''

    def forward_v2(self):
        float kp, p, p_ant, ki, i, kd, d, errorPID
        float vel_base = 0.5
        p,p_ant,i,d=0
        kp=0
        ki=0
        kd=0
        self.__currmov=1
        Robot.forward(self.__speedL,self.__speedR)

      




#W = Willy(left=(17,18), right=(22,23), speed=0.5, sonar=(4,15))

#W.forward(2)
#W.right(90)
#W.forward(1)

#W.forwardClick()
#time.sleep(1)
#W.stop()
