from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt, Signal

from controller.home_controller import Controller
from view.buttons.add_btn import AddBtn
from view.buttons.action_btn import ActionBtn


class HomePanel(QWidget):
    open_chat_requested = Signal(str)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.controller = Controller(self)
        self._build_ui()
        self._bind_events()


    def _build_ui(self):
        # top bar
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("Agentic Antivirus")
        title_label.setObjectName("titleLabel")
        title_label.setFixedHeight(40)
        title_label.setAlignment(Qt.AlignCenter)

        top_layout.addStretch()
        top_layout.addWidget(title_label)
        top_layout.addStretch()

        # chat input
        chat_layout = QHBoxLayout()
        chat_layout.setContentsMargins(10, 0, 10, 0)
        chat_layout.setSpacing(8)

        self.add_button = AddBtn()

        self.chat_input = QLineEdit()
        self.chat_input.setObjectName("chatInput")
        self.chat_input.setPlaceholderText("Scrivi un messaggio...")
        self.chat_input.setMinimumHeight(36)

        self.send_button = ActionBtn("→", "sendButton")

        chat_layout.addWidget(self.add_button)
        chat_layout.addWidget(self.chat_input, 1)
        chat_layout.addWidget(self.send_button)

        # bottom bar
        bottom_layout = QHBoxLayout()

        hint_label = QLabel("Seleziona una cartella da scansionare oppure chiedi all'assistente.")
        hint_label.setObjectName("hintLabel")
        hint_label.setMinimumWidth(500)
        hint_label.setAlignment(Qt.AlignHCenter)
        hint_label.setWordWrap(True)
        hint_label.setContentsMargins(15, 15, 15, 15)

        bottom_layout.addStretch()
        bottom_layout.addWidget(hint_label)
        bottom_layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(chat_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(bottom_layout)

    def _bind_events(self):
        self.add_button.clicked.connect(lambda _checked=False: self.controller.select_file())
        self.send_button.clicked.connect(self._open_chat_panel)
        self.chat_input.returnPressed.connect(self._open_chat_panel)


    def _open_chat_panel(self, _checked=False):
        message = self.chat_input.text().strip()
        self.chat_input.clear()
        self.open_chat_requested.emit(message)