from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QScrollArea, QVBoxLayout, QWidget

from view.buttons.add_btn import AddBtn
from view.buttons.action_btn import ActionBtn


class ChatPanel(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.reply_provider = None
        self._build_ui()
        self._bind_events()


    def _build_ui(self):
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)

        self.back_button = ActionBtn("←", "backButton")

        title_label = QLabel("Chat Assistant")
        title_label.setObjectName("chatTitle")
        title_label.setAlignment(Qt.AlignCenter)

        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addSpacing(self.back_button.sizeHint().width())

        self.messages_scroll = QScrollArea()
        self.messages_scroll.setObjectName("messagesScroll")
        self.messages_scroll.setWidgetResizable(True)

        messages_container = QWidget()
        messages_container.setObjectName("messagesContainer")
        self.messages_layout = QVBoxLayout(messages_container)
        self.messages_layout.setContentsMargins(12, 12, 12, 12)
        self.messages_layout.setSpacing(10)
        self.messages_layout.addStretch()
        self.messages_scroll.setWidget(messages_container)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(10, 0, 10, 10)
        input_layout.setSpacing(8)

        self.add_button = AddBtn()

        self.chat_input = QLineEdit()
        self.chat_input.setObjectName("chatInput")
        self.chat_input.setPlaceholderText("Scrivi un messaggio...")
        self.chat_input.setMinimumHeight(36)

        self.send_button = ActionBtn("→", "sendButton")

        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.chat_input, 1)
        input_layout.addWidget(self.send_button)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.messages_scroll, 1)
        main_layout.addLayout(input_layout)


    def _bind_events(self):
        self.back_button.clicked.connect(self._request_back)
        self.send_button.clicked.connect(self._send_message)
        self.chat_input.returnPressed.connect(self._send_message)


    def open_with_message(self, message: str):
        self.chat_input.setFocus()
        if message:
            self.chat_input.setText(message)
            self._send_message()


    def _request_back(self, _checked=False):
        self.back_requested.emit()


    def _send_message(self, _checked=False):
        text = self.chat_input.text().strip()
        if not text:
            return

        self.chat_input.clear()
        self.add_message(text, is_user=True)
        self.add_message(self._assistant_reply(text), is_user=False)


    def add_message(self, text: str, is_user: bool):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(560)
        bubble.setObjectName("userMessage" if is_user else "assistantMessage")

        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)

        if is_user:
            row_layout.addStretch()
            row_layout.addWidget(bubble)
        else:
            row_layout.addWidget(bubble)
            row_layout.addStretch()

        row_widget = QWidget()
        row_widget.setLayout(row_layout)

        insert_at = self.messages_layout.count() - 1
        self.messages_layout.insertWidget(insert_at, row_widget)
        QTimer.singleShot(0, self._scroll_to_bottom)


    def _assistant_reply(self, _: str) -> str:
        if self.reply_provider is None:
            return "Risposta assistente."

        try:
            response = self.reply_provider(_)
        except Exception as exc:
            return f"Errore assistant: {exc}"

        return str(response).strip() or "Non sono in grado di aiutarti o risponderti."


    def set_reply_provider(self, reply_provider):
        self.reply_provider = reply_provider


    def _scroll_to_bottom(self):
        scroll_bar = self.messages_scroll.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())