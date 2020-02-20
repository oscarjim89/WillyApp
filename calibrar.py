from time import sleep
from Willy import *
W = Willy(left=(17,18), right=(22,23), speed=1, sonar=(4,15))

W.forwardClick()
sleep(10)
W.stopClick()
