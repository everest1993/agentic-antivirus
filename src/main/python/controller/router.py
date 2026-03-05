"""
Classe di navigazione tra i pannelli
"""
class Router:
    def __init__(self, stack, home_panel, chat_panel):
        self.stack = stack
        self.home_panel = home_panel
        self.chat_panel = chat_panel

    def navigate_home(self):
        if self.stack.currentWidget() is self.home_panel:
            return
        
        self.stack.setCurrentWidget(self.home_panel)

    def navigate_chat(self):
        if self.stack.currentWidget() is self.chat_panel:
            return
        
        self.stack.setCurrentWidget(self.chat_panel)