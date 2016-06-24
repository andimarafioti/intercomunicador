# coding: utf-8
import os
import threading

__author__ = 'andres'


def record_until_interrupt(file_name):
    print 'Ha comenzado la grabación'
    command = "arecord -f cd -D plughw:0,0 " + file_name
    os.system(command)  # grabar audio hasta que lo interrumpas


def play_file(file_name):
    command = "aplay -D plughw:0,0 " + file_name
    os.system(command)  # reproducirlo


def user_interrupt(wait_event):
    global recordThread
    a = input('Presione la tecla Enter para finalizar la grabación')
    recordThread.shutdown = True
    recordThread._Thread__stop()
    wait_event.set()

WaitEvent = threading.Event()

RecordFlag = True

file_name = 'test.wav'

recordThread = threading.Thread(target=record_until_interrupt, args=[file_name])
recordThread.start()

userInputThread = threading.Thread(target=user_interrupt, args=[WaitEvent])
userInputThread.start()

WaitEvent.wait()
WaitEvent.clear()

play_file(file_name)

print "Todo salió bien"
