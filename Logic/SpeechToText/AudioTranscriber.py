import os
import whisper
import time

class AudioTranscriber:
    def __init__(self, output_text_file, wav_dir="wav", model_name="large-v3"):
        self.output_text_file = output_text_file

        # Dossier d'entrée
        self.input_wav_dir = os.path.abspath(wav_dir)
        if not os.path.isdir(self.input_wav_dir):
            raise FileNotFoundError(f"Dossier introuvable: {self.input_wav_dir}")

        # Charger le modèle Whisper
        try:
            self.model = whisper.load_model(model_name)
            if self.model is None:
                raise RuntimeError("Échec du chargement du modèle Whisper.")
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement du modèle Whisper: {e}")


    def get_oldest_audio_file(self):
        # Lister fichiers .wav et .mp3
        audio_files = [
            f for f in os.listdir(self.input_wav_dir)
            if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))
        ]

        if not audio_files:
            while not audio_files:
                try:
                    audio_files = [
                        f for f in os.listdir(self.input_wav_dir)
                        if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))
                    ]
                except:
                    time.sleep(2)

        full_paths = [os.path.join(self.input_wav_dir, f) for f in audio_files]
        oldest_file = min(full_paths, key=os.path.getmtime)
        print(f"Fichier le plus ancien: {oldest_file}")
        return oldest_file

    def transcribe_audio_file(self, audio_file, language="fr"):
        print(f"Transcription de {audio_file} ...")
        result = self.model.transcribe(
            audio_file,
            fp16=False,
            language=language
        )
        return result.get("text", "")

    def write_transcription_to_file(self, transcription):
        os.makedirs(os.path.dirname(self.output_text_file) or ".", exist_ok=True)
        with open(self.output_text_file, "a", encoding="utf-8") as f:
            f.write(transcription)

    def delete_file(self, audio_file):
        try:
            full_path = os.path.abspath(audio_file)
            print(f"Tentative de suppression : {full_path}")
            os.remove(full_path)
            print("Fichier supprimé avec succès.")
        except FileNotFoundError:
            print(f"Fichier introuvable : {audio_file}")
        except PermissionError:
            print(f"Pas la permission de supprimer : {audio_file}")
        except Exception as e:
            print(f"Impossible de supprimer {audio_file}: {e}")

    def transcribe_oldest_audio(self):
        audio_path = self.get_oldest_audio_file()
        if not audio_path:
            return

        try:
            transcription = self.transcribe_audio_file(audio_path, language="fr")
            self.write_transcription_to_file(transcription)
            print(f"Transcription écrite dans {self.output_text_file}")
            self.delete_file(audio_path)
        except FileNotFoundError as e:
            print("Erreur: FFmpeg introuvable. Installez FFmpeg et/ou ajoutez-le au PATH.")
            print(e)
        except Exception as e:
            print(f"Erreur pendant la transcription: {e}")
