import pyaudio
from Logic.Vocal_Gestion.ListenerAudio import ListenerAudio
from Logic.Vocal_Gestion.Stack.StackWav import StackWav
from Logic.SpeechToText.AudioTranscriber import AudioTranscriber
from pynput import keyboard
import os
import threading

class AudioListenerManager:
    def __init__(self):
        self.listener_bool = True
        self.stack = StackWav()
        self.listener_audio = ListenerAudio(
            chunk=1024, 
            sample_format=pyaudio.paFloat32, 
            channels=1, 
            fs=96000, 
            seconds=2, 
            filename="output.wav",
            p=pyaudio.PyAudio(),
            stack=self.stack
        )
        
        # Initialize keyboard listener for stopping the audio listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()

    def on_press(self, key):
        """Handle key press events, specifically stopping on ESC key."""
        if key == keyboard.Key.esc:
            self.listener_bool = False  # Stop the listener

    def start_listening(self):
        """Start the audio listening process."""
        while self.listener_bool:
            self.listener_audio.StartAudio()
        
        print(self.stack.stack.__str__())

    def run(self):
        """Method to start the whole listening process and manage the thread."""
        self.keyboard_listener.join()  # Wait for keyboard listener to stop

    def AudioTranscriber(self):
        output_text_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Transcription", "transcription.txt")
        
        transcriber = AudioTranscriber(output_text_file)
        while self.listener_bool:
            if os.path.exists('wav'):
                transcriber.transcribe_oldest_audio()

if __name__ == '__main__':
    audio_listener_manager = AudioListenerManager()
    AudioThread = threading.Thread(target=audio_listener_manager.start_listening)
    TranscriberThread = threading.Thread(target=audio_listener_manager.AudioTranscriber)

    AudioThread.start()
    TranscriberThread.start()

    AudioThread.join()
    TranscriberThread.join()
