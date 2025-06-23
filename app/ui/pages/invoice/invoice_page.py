from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import decimal

# Import tab classes
from .tabs.select_service_tab import SelectServiceTab
from .tabs.customer_tab import CustomerTab
from .tabs.payment_details_tab import PaymentDetailsTab
from .tabs.overview_tab import OverviewTab
from .tabs.receipt_tab import ReceiptTab

class InvoicePage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(InvoicePage, self).__init__(parent, title="Invoice", user_info=user_info)
        self.initializeInvoiceData()
        # Add a flag to track if a transaction is in progress
        self.transaction_in_progress = False
        # Add a flag to track if the current transaction has been completed
        self.invoice_completed = False

    def initializeInvoiceData(self):
        """Initialize the invoice data dictionary to be shared between tabs"""
        self.invoice_data = {
            "service": None,
            "customer": {
                "name": "",
                "phone": "",
                "gender": "",
                "city": ""
            },
            "payment": {
                "method": "Cash",
                "discount_percentage": decimal.Decimal('0.00'),
                "discount_amount": decimal.Decimal('0.00'),
                "base_amount": decimal.Decimal('0.00'),
                "total_amount": decimal.Decimal('0.00'),
                "coupon_code": ""
            },
            "or_number": "",
            "transaction_id": None,
            "transaction_date": None
        }
    
    def createContent(self):
        # Content area
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        # Create the tabs widget
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(self.get_tab_style())
        
        # Create custom tabs
        self.select_service_tab = SelectServiceTab(self)
        self.customer_tab = CustomerTab(self)
        self.payment_details_tab = PaymentDetailsTab(self)
        self.overview_tab = OverviewTab(self)
        self.receipt_tab = ReceiptTab(self)
        
        # Add tabs to the tab widget
        self.tabs.addTab(self.select_service_tab, "Select Service")
        self.tabs.addTab(self.customer_tab, "Customer")
        self.tabs.addTab(self.payment_details_tab, "Payment Details")
        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.receipt_tab, "Receipt")
        
        # Disable tabs until required data is entered
        self.tabs.setTabEnabled(1, False)  # Customer tab
        self.tabs.setTabEnabled(2, False)  # Payment Details tab
        self.tabs.setTabEnabled(3, False)  # Overview tab
        self.tabs.setTabEnabled(4, False)  # Receipt tab
        
        # Connect tab changed signal
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
        
        # Don't disable navigation until a service is actually selected
        # The navigation will be disabled in the select_service method when a service is chosen
        self.transaction_in_progress = False
    
    def on_tab_changed(self, index):
        """Handle tab change events to update data"""
        if index == 3:  # Overview tab
            self.overview_tab.updateOverview()
        elif index == 4:  # Receipt tab
            self.receipt_tab.generateReceipt()
    
    def enable_next_tab(self, current_tab_index):
        """Enable the next tab after completing current tab requirements"""
        if current_tab_index < self.tabs.count() - 1:
            self.tabs.setTabEnabled(current_tab_index + 1, True)
    
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
            QTabBar::tab:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
        """
    
    def cancel_transaction(self):
        """Cancel the current transaction"""
        # Only ask for confirmation if we've selected a service
        if self.invoice_data["service"] is not None:
            reply = QtWidgets.QMessageBox.question(
                self,
                "Cancel Transaction",
                "Are you sure you want to cancel this transaction?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.No:
                return False
        
        # Reset the invoice data
        self.reset_invoice()
        
        # Signal that the transaction is no longer in progress
        self.transaction_in_progress = False
        self.invoice_completed = False
        
        # Re-enable navigation in the main window
        if self.parent and hasattr(self.parent, 'enable_navigation'):
            self.parent.enable_navigation()
        
        return True

    def reset_invoice(self):
        """Reset the invoice data and tabs"""
        self.initializeInvoiceData()
        self.select_service_tab.reset()
        self.customer_tab.reset()
        self.payment_details_tab.reset()
        self.overview_tab.reset()
        self.receipt_tab.reset()
        
        # Disable tabs
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)
        self.tabs.setTabEnabled(4, False)
        
        # Return to first tab
        self.tabs.setCurrentIndex(0)
        
        # After resetting everything
        # Signal that the transaction is no longer in progress
        self.transaction_in_progress = False