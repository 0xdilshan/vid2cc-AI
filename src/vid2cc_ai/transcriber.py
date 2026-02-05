import whisper
import torch
import warnings

class Transcriber:
    def __init__(self, model_size="base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Suppress FP16 warning
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
        
        # Suppress the Translation Timestamp warning
        warnings.filterwarnings("ignore", message="Word-level timestamps on translations may not be reliable")

        self.model = whisper.load_model(model_size, device=self.device)

    def transcribe(self, audio_path: str, task: str = "transcribe"):
        """
        Transcribes audio file.
        task: 'transcribe' (default) or 'translate' (translates to English)
        """
        # Check for FP16 support
        use_fp16 = (self.device == "cuda")

        # word_timestamps=True - whisper hack for getting granular syncing
        return self.model.transcribe(
            audio_path, 
            task=task, 
            verbose=False, 
            word_timestamps=True,
            fp16=use_fp16
        )['segments']