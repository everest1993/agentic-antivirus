from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from model.ml_model import build_model
from model.feature_extractor import extract_ember_features
from model.assistant import Assistant


class Controller:
    def __init__(self, panel):
        self.panel = panel
        self.model = build_model()
        self.assistant = None
        self.selected_path = None


    def select_file(self):
        start_dir = str(Path.home())
        file_path, _ = QFileDialog.getOpenFileName(
            self.panel,
            "Seleziona file",
            start_dir,
            "All files (*.*)",
        )

        if not file_path:
            return None

        resolved = str(Path(file_path).expanduser().resolve())
        self.selected_path = resolved

        if hasattr(self.panel, "chat_input"):
            self.panel.chat_input.setText(resolved)

        return resolved
    

    def classify_file(self, file_path=None, threshold=0.5):
        target = file_path or self.selected_path

        if not target:
            raise ValueError("Nessun file selezionato.")

        resolved = str(Path(target).expanduser().resolve())
        features = extract_ember_features(resolved)
        probability = float(self.model.predict(features[None, :], verbose=0)[0][0])

        if probability >= threshold:
            return resolved, f"Potenziale malware (score={probability:.3f})"
        
        return resolved, f"File ok (score={probability:.3f})"
        

    def chat_with_assistant(self, message): # aggiungere thread per non freezare la GUI
        if self.assistant is None:
            self.assistant = Assistant()
            
        return self.assistant.chat(message)