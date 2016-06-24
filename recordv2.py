import pyaudio
import wave, sys, threading

from Tkinter import *


class DSP(threading.Thread):
    def __init__(self, ID, name, guiname):
        threading.Thread.__init__(self)
        self.threadID = ID
        self.name = name
        self.guiname = guiname  # este es del tipo APP de Tkinter


class DSPstart(DSP):
    def run(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        WAVE_OUTPUT_FILENAME = "file-" + str(count) + ".wav"

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        frames = []

        while isRecording:
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        self.guiname.s_String.set("Termino de grabar")


class DSPplay(DSP):
    def run(self):
        self.guiname.s_String.set("Reproduciendo...")
        CHUNK = 1024
        wf = wave.open("file-" + str(count) + ".wav", 'rb')
        play = pyaudio.PyAudio()
        stream = play.open(format=
                           play.get_format_from_width(wf.getsampwidth()),
                           channels=wf.getnchannels(),
                           rate=wf.getframerate(),
                           output=True)
        data = wf.readframes(CHUNK)
        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.close()
        play.terminate()


class App:
    def __init__(self, master, name):
        frame = Frame(master)
        frame.pack()
        self.name = name

        self.record = Button(frame,
                             text="GRABAR",
                             command=self.init_record)
        self.record.pack(side=LEFT)

        self.end = Button(frame,
                          text="FINALIZAR",
                          command=self.end_record)
        self.end.pack(side=LEFT)
        self.play = Button(frame,
                           text="REPRODUCIR",
                           command=self.play_record)
        self.play.pack(side=LEFT)
        self.button = Button(frame,
                             text="QUIT", fg="red",
                             command=frame.quit)
        self.button.pack(side=LEFT)
        self.s_String = StringVar()
        self.s_String.set("Standing By...")

        self.SLabel = Label(frame, textvariable=self.s_String)
        self.SLabel.pack(side=LEFT)

    def init_record(self):
        self.s_String.set("Grabando")
        global count
        count += 1
        thread = DSPstart(count, "thread-" + str(count), self)
        thread.start()

    def end_record(self):
        global isRecording
        isRecording = False

    def play_record(self):
        thread = DSPplay(count, "thread-" + str(count), self)
        thread.start()


count = 0
isRecording = True

root = Tk()
root.title("Grabador 1.0 (L)")
app = App(root, "grabador")
root.mainloop()
