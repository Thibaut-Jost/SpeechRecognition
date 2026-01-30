"""
Module de gestion pour l'enregistrement et l'écoute de l'utilisateur
"""
import sounddevice as sd
import webrtcvad
from filters_audio import FiltersAudio
from post_buffer_whisper import PostBufferWhisper


class Listener():
    """Class permettant l'écoute et l'enregistrement de l'utilisateur 
    """
    vad:webrtcvad.Vad
    filters:FiltersAudio #A utiliser si imprecision
    buffer:bytearray
    ms_latency:int
    whisper:PostBufferWhisper

    def __init__(self):
        self.filters = FiltersAudio()
        self.vad = webrtcvad.Vad()
        self.buffer = bytearray()
        self.ms_latency = 0
        self.whisper = PostBufferWhisper()

    def run(self):
        """Permet de lancer l'écoute de l'utilisateur et son enregistrement
        """

    def detect_voice(self):
        """
        Fonction Principale :
        On detecte la voix de l'utilisateur de mannière async via un thread
        les résultats sont directement envoyés au modèle d'analyse
        """
        fs:int =48000 # Pas changer (à automatiser au cas où)
        frame_ms: int = 10  # ms
        frame_samples:int = int(fs * frame_ms / 1000)
        vad = webrtcvad.Vad(3)

        #mic selection (A MODIFIER POUR AUTOMATISER)
        #print(sd.query_devices())
        sd.default.device = (31, 21)

        #-----FRAME SETTER-----
        # ici on laisse en int16 car le model n'attend que des integers
        # un float rends du bruit blanc capter comme des signaux speech
        with sd.InputStream(samplerate=fs, channels=1, dtype='int16',blocksize=frame_samples) as stream:
            while True:
                data, overflowed = stream.read(frame_samples)   # data shape (160, 1), int16
                frame_bytes = data.tobytes()                   # <- EXACT format for webrtcvad
                is_speech = vad.is_speech(frame_bytes, fs)
                if is_speech:
                    # On réinitialise la latence quand il y a un "blanc"
                    # puis on rajoute dansle buffer la frame de 10 ms
                    self.ms_latency = 0
                    self.buffer.extend(frame_bytes)
                else:
                    # On rajoute la latence pour regarder le temps de "blanc"
                    self.ms_latency += frame_ms
                    # Si le "blanc" est supérieur à 500 ms on considère que la phrase est fini
                    if self.ms_latency >= 500:
                        buffer_ms = (len(self.buffer) / (fs * 2)) * 1000
                        #On regarde si le buffer contient plus de 300ms de contenu (valeur arbitraire)
                        if buffer_ms >= 300:
                            # On envoie le buffer complet
                            self.whisper.analyse_buffer(self.buffer)
                        # Puis on réinitialise le buffer et ms_lantency pour la phrase suivante
                        self.buffer.clear()
                        self.ms_latency = 0



_listener:Listener = Listener()
_listener.detect_voice()
