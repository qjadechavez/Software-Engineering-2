from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector
from datetime import datetime

# Import the classes from the suppliers folder
from .style_factory import StyleFactory
from .table_factory import TableFactory
from .control_panel_factory import ControlPanelFactory
from .dialogs import SupplierDialog
from .tabs.suppliers_tab import SuppliersTab

class SuppliersPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(SuppliersPage, self).__init__(parent, title="Suppliers", user_info=user_info)
        
    def createContent(self):
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        # Create the tabs widget similar to inventory page
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(StyleFactory.get_tab_style())
        
        # Create tab components
        self.suppliers_tab = SuppliersTab(self)
        
        # Add the tabs to the tab widget
        self.tabs.addTab(self.suppliers_tab, "Suppliers")
        
        # Connect the tab change signal
        self.tabs.currentChanged.connect(self.handle_tab_change)
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
    
    def show_error_message(self, message):
        """Show error message dialog"""
        QtWidgets.QMessageBox.critical(self, "Error", message)
    
    def handle_tab_change(self, index):
        """Handle changing between tabs"""
        if index == 0:  # Suppliers tab
            # Force complete rebuild - this ensures table is properly refreshed
            QtCore.QTimer.singleShot(50, self.suppliers_tab.rebuild_table)
        # Add other tabs as needed