"""
Controller del pannello home
"""
from pathlib import Path
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Slot, QObject

from model.ml_model import build_model
from model.feature_extractor import extract_ember_features


class HomeController(QObject): # eredita da QObject per permettere l'invocazioine di select_file
    def __init__(self, panel = None):
        super().__init__()
        self.panel = panel # pagina home
        self.model = build_model() # modello di classificazione
        self.assistant = None # agente llm
        self.dubious_threshold = 0.5
        self.dangerous_threshold = 0.65


    @Slot(result=str)
    def select_file(self):
        """
        Apre il file picker per la selezione di file.
        Il decorer Slot fa in modo che il metodo possa essere invocato da un thread differente.
        """
        start_dir = str(Path.home())
        file_path, _ = QFileDialog.getOpenFileName(
            self.panel,
            "Seleziona file",
            start_dir,
            "All files (*.*)",
        )
    
        if file_path:
            return str(Path(file_path).expanduser().resolve())

        return ""


    def _risk_from_probability(self, probability):
        """
        Soglie di classificazione
        """
        if probability >= self.dangerous_threshold:
            return "dangerous", "Pericoloso"
        if probability >= self.dubious_threshold:
            return "dubious", "Dubbio"
        return "safe", "Sicuro"


    def classify_file(self, file_path=None):
        """
        classifica un file attraverso il modello keras
        """
        target = file_path
        resolved = str(Path(target).expanduser().resolve())
        features = extract_ember_features(resolved)

        probability = float(self.model.predict(features[None, :], verbose=0)[0][0])
        risk_key, risk_label = self._risk_from_probability(probability)

        return resolved, probability, risk_key, risk_label


    def handle_add_clicked(self):
        """
        Gestione del click su '+' nel pannello home
        """
        selected_path = self.select_file()

        if not selected_path or self.panel is None:
            return

        try:
            _, _, risk_key, risk_label = self.classify_file(selected_path)
            file_name = Path(selected_path).name or str(selected_path)

            self.panel.set_scan_status(risk_key, f"Il file {file_name} è {risk_label.lower()}.", True)
        except Exception as exc:
            file_name = Path(selected_path).name or str(selected_path)
            self.panel.set_scan_status("error", f"Errore scansione per il file {file_name}: {exc}", False)


    def handle_open_chat(self):
        """
        Apre la pagina di chat in un thread separato
        """
        if self.panel is None:
            return

        message = self.panel.chat_input.text().strip()
        self.panel.chat_input.clear()
        self.panel.open_chat_requested.emit(message)


    def chat_with_assistant(self, message):
        """
        Inizializza il modello Ollama e inizia la conversazione
        """
        if self.assistant is None:
            from model.assistant import Assistant # lazy import per evitare import circolare

            self.assistant = Assistant(controller=self)

        return self.assistant.chat(message)
