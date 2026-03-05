"""
Controller del pannello di chat.
"""
from PySide6.QtCore import QObject, QThread, Qt, Signal, Slot


class _ReplyWorker(QObject):
    # emesso quando la risposta e' pronta o in caso di errore
    finished = Signal(str)

    def __init__(self, reply_provider, message: str):
        super().__init__()
        self.reply_provider = reply_provider
        self.message = message


    @Slot()
    def run(self):
        # il worker gira in un thread secondario per non bloccare la GUI.
        if self.reply_provider is None:
            self.finished.emit("Assistente non disponibile.")
            return
        try:
            reply = str(self.reply_provider(self.message)).strip()
        except Exception as exc:
            reply = f"Errore: {exc}"
        self.finished.emit(reply or "Non sono in grado di aiutarti o risponderti.")


class ChatController(QObject):
    def __init__(self, panel, reply_provider=None):
        super().__init__(panel)
        self.panel = panel
        self.reply_provider = reply_provider
        self._thread = None
        self._worker = None
        self._typing_bubble = None # bubble temporanea "..."


    def handle_back_requested(self):
        self.panel.back_requested.emit()


    def handle_send_message(self):
        text = self.panel.chat_input.text().strip()

        if not text or self._thread is not None:
            return
        
        self.panel.chat_input.clear()
        self.panel.add_message(text, is_user=True)
        self.panel.scroll_to_bottom()

        self.panel.set_input_enabled(False)
        self._typing_bubble = self.panel.add_message("...", is_user=False)
        self.panel.scroll_to_bottom()
        self._start_worker(text)


    def _start_worker(self, message: str):
        """
        Inizializza un worker su thread dedicato e esegue cleanup automatico a fine lavoro
        """
        thread = QThread(self)
        worker = _ReplyWorker(self.reply_provider, message)
        worker.moveToThread(thread)
        thread.started.connect(worker.run, Qt.QueuedConnection)

        worker.finished.connect(self._on_reply_ready, Qt.QueuedConnection)
        worker.finished.connect(thread.quit, Qt.QueuedConnection)
        worker.finished.connect(worker.deleteLater)

        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._on_worker_finished, Qt.QueuedConnection)

        self._thread = thread
        self._worker = worker

        thread.start()


    def _on_reply_ready(self, reply: str):
        """
        Se esiste la bubble typing, la rimpiazza con la risposta finale
        """
        if self._typing_bubble is not None:
            self._typing_bubble.setText(reply)
            self.panel.scroll_to_bottom()
            self._typing_bubble = None
        else:
            self.panel.add_message(reply, is_user=False)
            self.panel.scroll_to_bottom()

        self.panel.set_input_enabled(True) # riabilita l'input


    def _on_worker_finished(self):
        """
        Reset dei riferimenti per consentire richieste successive
        """
        self._worker = None
        self._thread = None