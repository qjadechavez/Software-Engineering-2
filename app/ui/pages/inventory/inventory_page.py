from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector

# Import the factory classes
from .style_factory import StyleFactory
from .table_factory import TableFactory
from .control_panel_factory import ControlPanelFactory

# Import tab components
from .tabs.overview_tab import OverviewTab
from .tabs.products_tab import ProductsTab
from .tabs.services_tab import ServicesTab
from .tabs.inventory_status_tab import InventoryStatusTab

class InventoryPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(InventoryPage, self).__init__(parent, title="Inventory", user_info=user_info)
        
    def createContent(self):
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(StyleFactory.get_tab_style())
        
        # Create tab components
        self.overview_tab = OverviewTab(self)
        self.products_tab = ProductsTab(self)
        self.services_tab = ServicesTab(self)
        self.inventory_status_tab = InventoryStatusTab(self)
        
        # Add the tabs to the tab widget
        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.products_tab, "Products")
        self.tabs.addTab(self.services_tab, "Services")
        self.tabs.addTab(self.inventory_status_tab, "Inventory Status")
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
        
        # Connect the tab change signal
        self.tabs.currentChanged.connect(self.handle_tab_change)
        
        # Set Overview tab as the default and load initial data
        self.load_initial_data()

    def load_initial_data(self):
        """Load initial data for all tabs"""
        self.update_overview_tab()
        self.products_tab.load_products()
        self.services_tab.load_services()
        self.inventory_status_tab.load_inventory()
        self.inventory_status_tab.update_analytics()

    def handle_tab_change(self, index):
        """Handle changing between tabs"""
        if index == 0:  # Overview tab
            self.update_overview_tab()
        elif index == 1:  # Products tab
            self.products_tab.load_products()
        elif index == 2:  # Services tab
            self.services_tab.load_services()
        elif index == 3:  # Inventory Status tab
            self.inventory_status_tab.load_inventory()
            self.inventory_status_tab.update_analytics()

    def update_overview_tab(self):
        """Update the overview dashboard with fresh data"""
        self.overview_tab.update_dashboard()

    def show_error_message(self, message):
        """Show error message dialog"""
        QtWidgets.QMessageBox.critical(self, "Error", message)
        
    def switch_to_inventory_status(self):
        """Switch to the inventory status tab"""
        # Find the index of the Inventory Status tab and switch to it
        inventory_status_index = self.tabs.indexOf(self.inventory_status_tab)
        self.tabs.setCurrentIndex(inventory_status_index)