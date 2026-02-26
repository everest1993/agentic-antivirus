import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QStackedWidget, QVBoxLayout, QWidget

from view.panels.chat_panel import ChatPanel
from view.panels.home_panel import HomePanel


class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._apply_stylesheet()
        self._bind_events()


    def _build_ui(self):
        self.home_panel = HomePanel()
        self.chat_panel = ChatPanel()
        self.chat_panel.set_reply_provider(self.home_panel.controller.chat_with_assistant)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.home_panel)
        self.stack.addWidget(self.chat_panel)
        self.stack.setCurrentWidget(self.home_panel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)


    def _bind_events(self):
        self.home_panel.open_chat_requested.connect(self._open_chat_panel)
        self.chat_panel.back_requested.connect(self._show_home_panel)


    def _open_chat_panel(self, message: str):
        self.stack.setCurrentWidget(self.chat_panel)
        self.chat_panel.open_with_message(message)


    def _show_home_panel(self):
        self.stack.setCurrentWidget(self.home_panel)


    def _apply_stylesheet(self):
        stylesheet_path = Path(__file__).resolve().parents[1] / "resources" / "style.css"
        if stylesheet_path.exists():
            self.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))


def main() -> int:
    app = QApplication(sys.argv)
    window = App()
    window.setWindowTitle("Agentic Antivirus")
    window.resize(800, 400)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())