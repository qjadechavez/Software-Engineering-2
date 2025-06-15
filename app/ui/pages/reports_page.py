from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage

class ReportsPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(ReportsPage, self).__init__(parent, title="Reports", user_info=user_info)
    
    def createContent(self):
        # Content area
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Placeholder message
        placeholder_label = QtWidgets.QLabel("Reports content")
        placeholder_label.setAlignment(QtCore.Qt.AlignCenter)
        placeholder_label.setFont(QtGui.QFont("Segoe UI", 14))
        placeholder_label.setStyleSheet("color: #888888;")
        
        self.content_layout.addWidget(placeholder_label)
        self.content_layout.addStretch()
        
        self.layout.addWidget(self.content_area)