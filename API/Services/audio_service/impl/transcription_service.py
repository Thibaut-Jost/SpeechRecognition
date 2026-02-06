"""
Service pour la transcription entre le controller et le model
"""
from API.Services.audio_service.interface.i_transcription_service import ITranscriptionService

from API.Model.model_voice_to_text.interface.extern_interface_whisper import ExternInterfaceWhisper
from API.Model.model_voice_to_text.impl.post_buffer_whisper import PostBufferWhisper

class TranscriptionService(ITranscriptionService):
    """
    Contient les fonction pour faire le lien entre le controller et le model
    """

    #Whisper est un model extern on l'init en singleton pour éviter de ce retrouver
    # avec des object trop conséquent
    #ATTENTION (penser à en faire un injection plus tard avec plusieurs service)
    whisper : ExternInterfaceWhisper

    def __init__(self):
        super().__init__()
        self.whisper = PostBufferWhisper()

    def transcribe_audio_to_text(self, voice_array: bytearray) -> str:
        """
        Permet de transcrire le buffer voice en texte
        
        :param self: Instance actuel du service
        :param voice_array: buffer contenant la voix de l'utilsateur
        :type voice_array: bytearray
        :return: Renvoie un simple texte décrivant ce que l'utilsateur à dit
        :rtype: str
        """
        return self.whisper.analyse_buffer(voice_array)
