"""
Module de gestion pour whisper
"""
import os
import faster_whisper as whisper
import numpy as np
from numpy.typing import NDArray
import librosa
from extern_interface_whisper import ExternInterfaceWhisper

class PostBufferWhisper(ExternInterfaceWhisper):
    """Class de gestion de buffer pour whisper

    Args:
        ExternInterfaceWhisper (abstractClass): Abstract class pour limiter l'accès à la class
    """
    whisper_model:whisper.WhisperModel

    def __init__(self):
        super().__init__()
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
        self.whisper_model = whisper.WhisperModel("base", device="cpu", compute_type="int8", use_auth_token=os.getenv("HF_TOKEN"))

    def __resampling(self, audio_float32:bytearray) -> bytearray:
        """
        permet de re-sampler le buffer pour passé de 48000 Hz à 16000
        """
        audio_float32_rs:np.ndarray  = librosa.resample(
            audio_float32,
            orig_sr=48000,
            target_sr=16000
        )
        return audio_float32_rs

    def analyse_buffer(self, buffer:bytearray):
        """_summary_

        Args:
            buffer (bytearray): _description_
        """
        audio_int16:NDArray[np.int16] = np.frombuffer(buffer, dtype=np.int16)
        # Conversion vers float32 normalisé (-1.0 à 1.0)
        audio_float32:NDArray[np.float32] = audio_int16.astype(np.float32) / 32768.0
        #resampling pour passé de 48000 Hz micro vers 16000
        audio_float32 = self.__resampling(audio_float32=audio_float32)
        # Transcription
        segments, info = self.whisper_model.transcribe(
            audio_float32,
            language="fr"
        )
        for segment in segments:
            print(segment.text)

    def get_last_input(self):
        """_summary_
        """
