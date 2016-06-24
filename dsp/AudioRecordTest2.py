# coding: utf8

import threading

from DSPConstructors import DSPRecord, DSPPlay

__author__ = 'andres'


def user_interrupt(wait_event):
    a = input('Presione la tecla Enter para finalizar la grabación\n')
    wait_event.set()


file_name = 'test.wav'
a_record = DSPRecord(file_name, 1)
a_record.start()

WaitEvent = threading.Event()

userInputThread = threading.Thread(target=user_interrupt, args=[WaitEvent])
userInputThread.start()

WaitEvent.wait()
WaitEvent.clear()

a_record.stop()

a_play = DSPPlay(file_name, 1)
a_play.start()


print "Todo salió bien"
