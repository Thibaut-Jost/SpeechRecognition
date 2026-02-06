"""Module interface pour whisper"""
from abc import ABC, abstractmethod

class ExternInterfaceWhisper(ABC):
    """Interface pour accéder au whisper

    Args:
        ABC (_type_): Met en place les abstract method
    """

    def __init__(self):
        pass

    @abstractmethod
    def analyse_buffer(self, buffer:bytearray):
        """Permet d'envoyer un buffer au modèle whisper

        Args:
            buffer (bytearray): buffer de frame_bytes
        """
