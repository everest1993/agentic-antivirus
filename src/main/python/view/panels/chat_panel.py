from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QScrollArea, QVBoxLayout, QWidget

from controller.chat_controller import ChatController
from view.buttons.action_btn import ActionBtn


class ChatPanel(QWidget):
    back_requested = Signal()

    def __init__(self, reply_provider=None, parent=None):
        super().__init__(parent)
        self.controller = ChatController(self, reply_provider=reply_provider)
        self._build_ui()
        self.back_button.clicked.connect(self.controller.handle_back_requested)
        self.send_button.clicked.connect(self.controller.handle_send_message)
        self.chat_input.returnPressed.connect(self.controller.handle_send_message)


    def _build_ui(self):
        self.back_button = ActionBtn("←", "backButton")
        self.title_label = QLabel("Chat Assistant")
        self.title_label.setObjectName("chatTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        top_layout.addWidget(self.title_label)
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

        self.chat_input = QLineEdit()
        self.chat_input.setObjectName("chatInput")
        self.chat_input.setPlaceholderText("Scrivi un messaggio...")
        self.chat_input.setMinimumHeight(36)
        self.send_button = ActionBtn("→", "sendButton")

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(10, 0, 10, 10)
        input_layout.setSpacing(8)
        input_layout.addWidget(self.chat_input, 1)
        input_layout.addWidget(self.send_button)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.messages_scroll, 1)
        main_layout.addLayout(input_layout)


    def open_with_message(self, message: str = ""):
        text = message.strip()

        if text:
            self.chat_input.setText(text)
            self.controller.handle_send_message()
            return
        
        self.chat_input.setFocus() # intercetta enter


    def add_message(self, text: str, is_user: bool):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(600)
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

        self.messages_layout.insertWidget(self.messages_layout.count() - 1, row_widget)
        
        return bubble


    def set_input_enabled(self, enabled: bool):
        self.chat_input.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
        
        if enabled:
            self.chat_input.setFocus()


    def scroll_to_bottom(self):
        def _apply_scroll():
            container = self.messages_scroll.widget()
            if container is not None:
                container.adjustSize()

            scrollbar = self.messages_scroll.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

        QTimer.singleShot(0, _apply_scroll)