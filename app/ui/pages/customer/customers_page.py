from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector

from .style_factory import StyleFactory
from .table_factory import TableFactory
from .control_panel_factory import ControlPanelFactory

from .tabs.customers_tab import CustomersTab

class CustomersPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(CustomersPage, self).__init__(parent, title="Customers", user_info=user_info)
    
    def createContent(self):
        # Content area
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        # Create the tabs widget
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(StyleFactory.get_tab_style())
        
        # Create tab components
        self.customers_tab = CustomersTab(self)
        
        # Add the tabs to the tab widget
        self.tabs.addTab(self.customers_tab, "Customers")
        
        # Connect tab changed signal to handle refreshes
        self.tabs.currentChanged.connect(self.handle_tab_change)
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
    
    def handle_tab_change(self, index):
        """Handle changing between tabs"""
        if index == 0:  # Customers tab
            # Force complete rebuild - this ensures table is properly refreshed
            QtCore.QTimer.singleShot(50, self.customers_tab.rebuild_table)
    
    def show_error_message(self, message):
        """Show error message dialog"""
        QtWidgets.QMessageBox.critical(self, "Error", message)