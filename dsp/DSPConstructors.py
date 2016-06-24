import pyaudio
import threading
import wave

__author__ = 'andres'


class AbstractDSP(object):
    def __init__(self, file_name, device_index):
        super(AbstractDSP, self).__init__()
        self.file_name = file_name
        self.device_index = device_index
        self._DSPThread = threading.Thread(target=self.function)

    def start(self):
        self._DSPThread.start()

    def getThread(self):
        return self._DSPThread

    def function(self):
        raise NotImplementedError


class DSPRecord(AbstractDSP):
    def __init__(self, file_name, device_index):
        super(DSPRecord, self).__init__(file_name, device_index)
        self.recording_flag = True
        self.wait_event = threading.Event()

    def function(self):
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 44100
        chunk = 512
        wave_output_filename = self.file_name

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=audio_format, channels=channels,
                            rate=rate, input=True,
                            input_device_index=self.device_index,
                            frames_per_buffer=chunk)
        frames = []

        print("\n* recording \n")
        while self.recording_flag:
            data = stream.read(chunk)
            frames.append(data)
        print("\n* done recording\n")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        wave_file = wave.open(wave_output_filename, 'wb')
        wave_file.setnchannels(channels)
        wave_file.setsampwidth(audio.get_sample_size(audio_format))
        wave_file.setframerate(rate)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

        self.wait_event.set()

    def stop(self):
        self.recording_flag = False
        self.wait_event.wait()
        self.wait_event.clear()


class DSPPlay(AbstractDSP):
    def __init__(self, file_name, device_index):
        super(DSPPlay, self).__init__(file_name, device_index)
        self.file_name = file_name

    def function(self):
        chunk = 512
        wf = wave.open(self.file_name, 'rb')
        play = pyaudio.PyAudio()
        stream = play.open(format=play.get_format_from_width(wf.getsampwidth()),
                           channels=wf.getnchannels(),
                           rate=wf.getframerate(),
                           output=True, output_device_index=self.device_index)

        data = wf.readframes(chunk)
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)

        stream.close()
        play.terminate()


