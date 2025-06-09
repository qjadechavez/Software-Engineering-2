from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage

class HelpPage(BasePage):
    def __init__(self, parent=None):
        super(HelpPage, self).__init__(parent)
        
    def setupUi(self):
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Header widget
        self.header_widget = QtWidgets.QWidget()
        self.header_widget.setFixedHeight(99)
        self.header_widget.setStyleSheet("background-color: rgba(35, 35, 35, 0.95);")
        self.layout.addWidget(self.header_widget)
        
        # Content area
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        
        # Add help content (placeholder for now)
        label = QtWidgets.QLabel("Help")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.content_layout.addWidget(label)
        
        self.layout.addWidget(self.content_widget)