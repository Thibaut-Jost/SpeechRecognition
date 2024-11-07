import pyaudio
import wave
from Logic.Vocal_Gestion.Stack.StackWav import StackWav
import random
import os

class ListenerAudio:
    
    def __init__(self,chunk,sample_format,channels,fs,seconds,filename,p,stack):
        self.chunk = chunk  # Record in chunks of 1024 samples
        self.sample_format = sample_format  # 16 bits per sample
        self.channels = channels
        self.fs = fs  # Record at 44100 samples per second
        self.seconds = seconds
        self.filename = filename
        self.p = p  # Create an interface to PortAudio
        self.stack = stack
    
    def StartAudio(self):
        self.p = pyaudio.PyAudio()
        print('Start Recording ...')
        
        stream = self.p.open(format=self.sample_format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True)
        
        frames = []  # Initialize array to store frames
        
        # Store data in chunks for 3 seconds
        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()
        print('... Finished recording')

        # Vérifier si le dossier 'wav' existe, sinon le créer
        if not os.path.exists('wav'):
            os.makedirs('wav')

        # Enregistrer les données enregistrées sous forme de fichier WAV
        self.filename = os.path.join('wav', str(random.randint(0, 1000000000)) + ".wav")
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        self.stack.StackAppend(self.filename)
        wf.close()

        