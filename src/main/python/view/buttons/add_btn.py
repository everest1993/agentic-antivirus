from PySide6.QtWidgets import QPushButton


class AddBtn(QPushButton):
    def __init__(self, symbol="+", parent=None):
        super().__init__(symbol, parent)
        self.setObjectName("addButton")
        self.setFixedSize(36, 36)