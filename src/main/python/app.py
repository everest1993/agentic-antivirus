import sys

from pathlib import Path
from PySide6.QtWidgets import QApplication, QStackedWidget, QVBoxLayout, QWidget

from view.panels.chat_panel import ChatPanel
from view.panels.home_panel import HomePanel
from controller.router import Router


class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.home_panel = HomePanel()
        self.chat_panel = ChatPanel(reply_provider=self.home_panel.controller.chat_with_assistant)

        # stack di pagine per alternare Home e Chat senza aprire nuove finestre
        self.stack = QStackedWidget()
        self.stack.addWidget(self.home_panel)
        self.stack.addWidget(self.chat_panel)
        self.stack.setCurrentWidget(self.home_panel) # mostra Home come pagina iniziale

        self.router = Router(self.stack, self.home_panel, self.chat_panel)

        layout = QVBoxLayout(self) # layout principale della finestra
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

        # stile CSS
        stylesheet_path = Path(__file__).resolve().parents[1] / "resources" / "style.css"
        self.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))

        # collegamento tra pannelli
        self.home_panel.open_chat_requested.connect(self._open_chat_panel)
        self.chat_panel.back_requested.connect(self._show_home_panel)


    def _open_chat_panel(self, message: str):
        """
        Navigazione verso il pannello di chat
        """
        self.router.navigate_chat()
        self.chat_panel.open_with_message(message)


    def _show_home_panel(self):
        """
        Navigazione verso il pannello home
        """
        self.home_panel.clear_scan_status() # ripristina la label di scansione
        self.router.navigate_home()


def main():
    app = QApplication(sys.argv)
    window = App() # finestra principale
    window.setWindowTitle("Agentic Antivirus") # titolo
    window.resize(800, 400) # dimensioni iniziali
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())