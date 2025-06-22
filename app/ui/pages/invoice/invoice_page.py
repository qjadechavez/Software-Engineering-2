from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage

class InvoicePage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(InvoicePage, self).__init__(parent, title="Invoice", user_info=user_info)
    
    def createContent(self):
        # Content area
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        # Create the tabs widget similar to suppliers page
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(self.get_tab_style())
        
        # Create 5 empty tabs
        self.setup_tab("Select Service")
        self.setup_tab("Customer")
        self.setup_tab("Payment Details")
        self.setup_tab("Overview")
        self.setup_tab("Receipt")
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
    
    def setup_tab(self, tab_name):
        """Setup an empty tab with the given name"""
        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout(tab)
        tab_layout.setContentsMargins(10, 15, 10, 10)
        
        # Add empty placeholder for now
        placeholder = QtWidgets.QLabel(f"{tab_name} content will go here")
        placeholder.setAlignment(QtCore.Qt.AlignCenter)
        placeholder.setStyleSheet("color: #888888; font-size: 14px;")
        tab_layout.addWidget(placeholder)
        
        # Add tab to the tab widget
        self.tabs.addTab(tab, tab_name)
    
    def get_tab_style(self):
        """Return the CSS styling for tabs"""
        return """
            QTabWidget::pane { 
                border: 1px solid #444; 
                background-color: #232323;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #343434;
                color: #ffffff;
                padding: 10px 30px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                min-width: 120px;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                border-bottom-color: #1a1a1a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
            }
        """