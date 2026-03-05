from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget

from controller.home_controller import HomeController
from view.buttons.action_btn import ActionBtn
from view.buttons.add_btn import AddBtn


class HomePanel(QWidget):
    open_chat_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = HomeController(self)
        self._build_ui()
        self.add_button.clicked.connect(self.controller.handle_add_clicked)
        self.send_button.clicked.connect(self.controller.handle_open_chat)
        self.chat_input.returnPressed.connect(self.controller.handle_open_chat)


    def _build_ui(self):
        self.title_label = QLabel("Agentic Antivirus")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setFixedHeight(40)
        self.title_label.setAlignment(Qt.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)
        top_layout.addStretch()
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()

        self.add_button = AddBtn()
        self.chat_input = QLineEdit()
        self.chat_input.setObjectName("chatInput")
        self.chat_input.setPlaceholderText("Scrivi un messaggio...")
        self.chat_input.setMinimumHeight(36)
        self.send_button = ActionBtn("→", "sendButton")

        chat_layout = QHBoxLayout()
        chat_layout.setContentsMargins(10, 0, 10, 0)
        chat_layout.setSpacing(8)
        chat_layout.addWidget(self.add_button)
        chat_layout.addWidget(self.chat_input, 1)
        chat_layout.addWidget(self.send_button)

        self.scan_status_label = QLabel("")
        self.scan_status_label.setObjectName("scanStatusLabel")
        self.scan_status_label.setProperty("status", "neutral")
        self.scan_status_label.setAlignment(Qt.AlignCenter)
        self.scan_status_label.setWordWrap(True)
        self.scan_status_label.setMinimumHeight(22)

        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(20, 0, 20, 0)
        status_layout.addWidget(self.scan_status_label, 1)

        self.hint_label = QLabel("Seleziona un file da scansionare oppure chiedi all'assistente.")
        self.hint_label.setObjectName("hintLabel")
        self.hint_label.setAlignment(Qt.AlignHCenter)
        self.hint_label.setWordWrap(True)
        self.hint_label.setContentsMargins(15, 15, 15, 15)
        self.hint_label.setMinimumWidth(600)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.hint_label)
        bottom_layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(chat_layout)
        main_layout.addLayout(status_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(bottom_layout)


    def set_scan_status(self, status: str, text: str, visible: bool):
        """
        Metodo per modificare la label di classificazione
        """
        self.scan_status_label.setText(text)
        self.scan_status_label.setProperty("status", status)
        self.scan_status_label.style().unpolish(self.scan_status_label)
        self.scan_status_label.style().polish(self.scan_status_label)
        self.scan_status_label.setVisible(visible)


    def clear_scan_status(self):
        self.set_scan_status("neutral", "", True)