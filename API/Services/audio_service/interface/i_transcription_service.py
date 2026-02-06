"""
Module interface pour le service de transcription
"""

from abc import ABC, abstractmethod

class ITranscriptionService(ABC):
    """
    Contient les fonction pour faire le lien entre le controller et le model
    """

    def __init__(self):
        pass

    @abstractmethod
    def transcribe_audio_to_text(self, voice_array: bytearray) -> str:
        """
        Permet de transcrire le buffer voice en texte
        
        :param self: Instance actuel du service
        :param voice_array: buffer contenant la voix de l'utilsateur
        :type voice_array: bytearray
        :return: Renvoie un simple texte décrivant ce que l'utilsateur à dit
        :rtype: str
        """
        pass
