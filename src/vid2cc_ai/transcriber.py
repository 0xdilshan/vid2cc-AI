import whisper
import torch

class Transcriber:
    def __init__(self, model_size="base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_size, device=self.device)

    def transcribe(self, audio_path: str, task: str = "transcribe"):
        """
        Transcribes audio file.
        task: 'transcribe' (default) or 'translate' (translates to English)
        """
        # word_timestamps=True - whisper hack for getting granular syncing
        return self.model.transcribe(
            audio_path, 
            task=task, 
            verbose=False, 
            word_timestamps=True
        )['segments']