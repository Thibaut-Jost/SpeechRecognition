import os
import whisper
import ffmpeg

class AudioTranscriber:
    def __init__(self, audio_directory, output_text_file):
        self.audio_directory = audio_directory
        self.output_text_file = output_text_file
        try:
            self.model = whisper.load_model("base")
            if self.model is None:
                raise ValueError("Échec du chargement du modèle Whisper.")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle : {e}")
            self.model = None  # Choisissez le modèle souhaité

    def get_oldest_audio_file(self):
        # Lister tous les fichiers audio dans le dossier
        audio_files = [f for f in os.listdir(self.audio_directory) if f.endswith(('.mp3', '.wav'))]
        
        if not audio_files:
            print("Aucun fichier audio trouvé dans le dossier.")
            return None

        # Créer des chemins complets pour les fichiers
        full_paths = [os.path.join(self.audio_directory, f) for f in audio_files]
        
        # Trier les fichiers par date de modification
        oldest_file = min(full_paths, key=os.path.getmtime)
        return oldest_file

    def transcribe_audio_file(self, audio_file):
        print(f"Transcribing {audio_file}...")
        result = self.model.transcribe(audio_file, fp16=False, language='french')
        return result["text"]

    def write_transcription_to_file(self, transcription):
        with open(self.output_text_file, 'w', encoding='utf-8') as f:
            f.write(transcription)

    def delete_oldest_file(self, audio_file):
        os.remove(audio_file)

    def transcribe_oldest_audio(self):

        
        oldest_audio_file = self.get_oldest_audio_file()
        
        if oldest_audio_file:
            transcription = self.transcribe_audio_file(oldest_audio_file)
            self.write_transcription_to_file(transcription)
            self.delete_oldest_file(oldest_audio_file)
            print(f"Transcription écrite dans {self.output_text_file}")

