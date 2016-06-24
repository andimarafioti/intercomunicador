# coding: utf-8
"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
import os

import pyaudio
import threading
import wave


def record(file_name):
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = file_name
    INPUT_DEVICE_INDEX = 1

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=INPUT_DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    while isRecording:
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def play_file(file_name):
    command = "aplay -D plughw:1,0 " + file_name
    os.system(command)  # reproducirlo


def user_interrupt(wait_event):
    global isRecording
    a = input('Presione la tecla Enter para finalizar la grabación')
    isRecording = False
    wait_event.set()

isRecording = True

WaitEvent = threading.Event()

file_name = 'test.wav'

recordThread = threading.Thread(target=record, args=[file_name])
recordThread.start()

userInterruptThread = threading.Thread(target=user_interrupt, args=[WaitEvent])
userInterruptThread.start()

WaitEvent.wait()
WaitEvent.clear()

play_file(file_name)

print "Todo salió bien"