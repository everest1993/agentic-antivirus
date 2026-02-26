from PySide6.QtWidgets import QPushButton


class ActionBtn(QPushButton):
    def __init__(self, symbol, obj_name, parent=None):
        super().__init__(symbol, parent)
        self.setObjectName(obj_name)
        self.setFixedHeight(36)