import whisper
import torch

class Transcriber:
    def __init__(self, model_size="base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_size, device=self.device)

    def transcribe(self, audio_path: str):
        # verbose=False enables the automatic progress bar in the console
        return self.model.transcribe(audio_path, verbose=False)['segments']