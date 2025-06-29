from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector

# Import the factory classes
from .style_factory import StyleFactory
from .table_factory import TableFactory
from .control_panel_factory import ControlPanelFactory

# Import tab components
from .tabs import DatabaseBackupTab, UserManagementTab

class MaintenancePage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(MaintenancePage, self).__init__(parent, title="Maintenance", user_info=user_info)
        self.user_info = user_info

    
    def createContent(self):
        """Create the normal maintenance page content for admin users"""
        # Content area
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        # Create the tabs widget
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(StyleFactory.get_tab_style())
        
        # Create tab components
        self.database_backup_tab = DatabaseBackupTab(self)
        self.user_management_tab = UserManagementTab(self)
        
        # Add the tabs to the tab widget
        self.tabs.addTab(self.database_backup_tab, "Database Backup")
        self.tabs.addTab(self.user_management_tab, "User Management")
        
        # Connect tab changed signal to handle refreshes
        self.tabs.currentChanged.connect(self.handle_tab_change)
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
        
        # Load initial data
        self.load_initial_data()
    
    def handle_tab_change(self, index):
        """Handle changing between tabs"""
        if hasattr(self, 'database_backup_tab') and hasattr(self, 'user_management_tab'):
            if index == 0:  # Database Backup tab
                self.database_backup_tab.load_table_info()
            elif index == 1:  # User Management tab
                self.user_management_tab.refresh_data()
    
    def load_initial_data(self):
        """Load initial data for all tabs"""
        try:
            # Only load data if we have the tabs (admin user)
            if hasattr(self, 'database_backup_tab') and hasattr(self, 'user_management_tab'):
                # Load data for the first tab (database backup)
                self.database_backup_tab.load_table_info()
                # Load data for user management tab
                self.user_management_tab.load_user_data()
        except Exception as e:
            print(f"Error loading initial maintenance data: {e}")
    
    def show_error_message(self, message):
        """Show error message dialog"""
        QtWidgets.QMessageBox.critical(self, "Error", message)
    
    def show_info_message(self, message):
        """Show info message dialog"""
        QtWidgets.QMessageBox.information(self, "Information", message)