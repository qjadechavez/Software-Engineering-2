from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage

class HelpPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(HelpPage, self).__init__(parent, title="Help", user_info=user_info)
    
    def createContent(self):
        # Content area - just an empty widget with a placeholder
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Set background color for the content area
        self.content_area.setStyleSheet("background-color: red;")
        
        # Placeholder message
        placeholder_label = QtWidgets.QLabel("Help content")
        placeholder_label.setAlignment(QtCore.Qt.AlignCenter)
        placeholder_label.setFont(QtGui.QFont("Segoe UI", 14))
        placeholder_label.setStyleSheet("color: #888888;")
        
        self.content_layout.addWidget(placeholder_label)
        self.content_layout.addStretch()
        
        self.layout.addWidget(self.content_area)