import threading
from time import sleep
from config import FILE_NAME
from dsp.DSPConstructors import DSPPlay, DSPRecord
from gui.mainView import MainView

__author__ = 'andres'

KillEvent = threading.Event()

dspPlay = DSPPlay(FILE_NAME, 1)
dspRecord = DSPRecord(FILE_NAME, 1)

menu = MainView()

sleep(2)
menu.downClicked()
sleep(2)
menu.downClicked()
sleep(2)
menu.downClicked()
sleep(2)
menu.upClicked()
sleep(2)
menu.upClicked()
sleep(2)
menu.upClicked()
sleep(2)
menu.upClicked()

KillEvent.wait()
