from gpiozero import InputDevice, OutputDevice
from time import sleep, time

trig = OutputDevice(4)
echo = InputDevice(15)

sleep(2)

def get_pulse_time():
	trig.on()
	sleep(0.00001)
	trig.off()
	
	while echo.is_active == False:
		pulse_start = time()
	while echo.is_active == True:
		pulse_end = time()
	
	sleep(0.06)
	
	return pulse_end - pulse_start

def calculate_distance(duration):
	speed = 343
	distance = speed * duration / 2
	return distance

while True:
        duration = get_pulse_time()
	distance = calculate_distance(duration)
        distance = distance * 100
	print(str(round(distance,1)) + "cm")
        sleep(4)
