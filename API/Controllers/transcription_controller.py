"""
Module controller pour transcription d'audio
"""
import http

from fastapi import APIRouter, Body

from API.Services.audio_service.interface.i_trasncription_service import ITranscriptionService
from API.Services.audio_service.impl.transcription_service import TranscriptionService

transcription_router = APIRouter(prefix="/v1/transcription")
transcription_service : ITranscriptionService = TranscriptionService()

@transcription_router.post("/transcribe", status_code=http.HTTPStatus.OK)
async def transcribe_audio_to_text(voice_array: bytes = Body(...)):
    """
    Permet de transformer un audio en texte
    
    :param voice_array: object de bytes
    :type voice_array: bytes
    """
    return transcription_service.transcribe_audio_to_text(bytearray(voice_array))
