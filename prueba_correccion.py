from odometer import odometer
from time import sleep

vel_base = 0.5
p=0
p_ant=0
i=0
d=0
kp=10
ki=0.5
kd=1
odo=odometer()
while (1):
    xo,yo=odo.getOdo()
    p=0-xo #-3.5
    i=i+p #-9.5
    d=p-p_ant #-7.5
    p_ant=p #-3.5
    if ((p*i)<0):
        i=0
    errorPID= (kp*p + ki*i + kd*d)/10 #-0.16
    #TODO: Asegurar-se de que el rang del errorPID sigui abs(0.5)
    if(errorPID>abs(0.15)):
        print (errorPID, vel_base-errorPID,vel_base+errorPID)
    sleep(5)
                
