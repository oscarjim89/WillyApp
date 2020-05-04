from desp2mongo import *
from odometer import *
from PrintMap import *
from time import sleep
from datetime import datetime

now = datetime.now()
j1 = journalDB("prova"+now.strftime("%H%M%S"))
o1 = odometer()

while True:
    try:
        x,y = o1.getOdo()
        j1.updateJournal(x,y)
        sleep(1)
    except KeyboardInterrupt:
        break

p1 = PrintMap(j1.getJournalid())

p1.printSVG()
