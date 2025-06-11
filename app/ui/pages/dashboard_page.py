from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(DashboardPage, self).__init__(parent, title="Dashboard", user_info=user_info)
    
    def createContent(self):
        # Scroll area (keeping the container, but not adding widgets to it)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background-color: #F5F5F5;")
        
        # Scroll content widget
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(20)
        
        # Add placeholder message
        placeholder_label = QtWidgets.QLabel("Dashboard content")
        placeholder_label.setAlignment(QtCore.Qt.AlignCenter)
        placeholder_label.setFont(QtGui.QFont("Segoe UI", 14))
        placeholder_label.setStyleSheet("color: #888888;")
        self.scroll_layout.addWidget(placeholder_label)
        
        # Add stretch to push placeholder to the top
        self.scroll_layout.addStretch()
        
        self.layout.addWidget(self.scroll_area)