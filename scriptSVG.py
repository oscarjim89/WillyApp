from desp2mongo import *
from odometer import *
from PrintMap import *
from time import sleep

j1 = journalDB("prova_020520201800")
o1 = odometer()
o1.activate()
p1 = PrintMap(j1.getJournalid())

while not KeyboardInterrupt:
    j1.updateJournal(o1.getOdo())
    sleep(2)

p1.printSVG()
