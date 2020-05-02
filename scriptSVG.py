from desp2mongo import *
from odometer import *
from PrintMap import *
from time import sleep

j1 = journalDB("prova_020520201800")
o1 = odometer()
p1 = PrintMap(j1.getJournalid())

while True:
    try:
        j1.updateJournal(o1.getOdo())
        sleep(2)
    except KeyboardInterrupt:
        break

p1.printSVG()
