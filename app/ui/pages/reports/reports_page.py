from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector

# Import the factory classes
from .style_factory import StyleFactory
from .table_factory import TableFactory
from .control_panel_factory import ControlPanelFactory

# Import tab components
from .tabs.delivered_products_tab import DeliveredProductsTab
from .tabs.alert_level_tab import AlertLevelTab
from .tabs.sales_report_tab import SalesReportTab
from .tabs.undelivered_products_tab import UndeliveredProductsTab
from .tabs.transaction_logs_tab import TransactionLogsTab
from .tabs.missing_products_tab import MissingProductsTab

class ReportsPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(ReportsPage, self).__init__(parent, title="Reports & Analytics", user_info=user_info)
        
    def createContent(self):
        # Content area
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)
        
        # Create the tabs widget
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(self.get_tab_style())
        
        # Create tabs
        self.delivered_products_tab = DeliveredProductsTab(self)
        self.alert_level_tab = AlertLevelTab(self)
        self.sales_report_tab = SalesReportTab(self)
        self.undelivered_products_tab = UndeliveredProductsTab(self)
        self.transaction_logs_tab = TransactionLogsTab(self)
        self.missing_products_tab = MissingProductsTab(self)
        
        # Add tabs to the tab widget
        self.tabs.addTab(self.delivered_products_tab, "📦 Delivered Products")
        self.tabs.addTab(self.alert_level_tab, "⚠️ Alert Level Report")
        self.tabs.addTab(self.sales_report_tab, "💰 Sales Report")
        self.tabs.addTab(self.undelivered_products_tab, "🚚 Undelivered Products")
        self.tabs.addTab(self.transaction_logs_tab, "📋 Transaction Logs")
        self.tabs.addTab(self.missing_products_tab, "❓ Missing Products")
        
        # Connect tab changed signal
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
        
        # Load initial data
        self.load_initial_data()
    
    def on_tab_changed(self, index):
        """Handle tab change events to refresh data"""
        current_tab = self.tabs.widget(index)
        if hasattr(current_tab, 'refresh_data'):
            current_tab.refresh_data()
    
    def load_initial_data(self):
        """Load initial data for all tabs"""
        try:
            # Load data for the first tab (delivered products)
            self.delivered_products_tab.load_delivered_products()
        except Exception as e:
            print(f"Error loading initial reports data: {e}")
    
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
                padding: 12px 25px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                min-width: 140px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                border-bottom-color: #1a1a1a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
            }
        """
    
    def show_error_message(self, message):
        """Show error message to user"""
        QtWidgets.QMessageBox.critical(self, "Error", message)
    
    def show_info_message(self, message):
        """Show info message to user"""
        QtWidgets.QMessageBox.information(self, "Information", message)