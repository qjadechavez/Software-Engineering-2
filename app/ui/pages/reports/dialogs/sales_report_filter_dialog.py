from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from .base_dialog import BaseDialog

class SalesReportFilterDialog(BaseDialog):
    """Dialog for filtering sales report data"""
    
    def __init__(self, parent=None, filter_state=None):
        super(SalesReportFilterDialog, self).__init__(parent, None, "Filter Sales Report")
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "amount_range": "All Amounts",
            "service": "All Services"
        }
        self.result_filter_state = self.filter_state.copy()
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_base_ui(450)
        
        self.header_label.setText("Filter Sales Report")
        
        # Date range filter
        date_label = QtWidgets.QLabel("Date Range:")
        self.date_combo = QtWidgets.QComboBox()
        self.date_combo.addItems([
            "All Time",
            "Today",
            "This Week", 
            "This Month",
            "Last 30 Days",
            "Last 90 Days",
            "This Year"
        ])
        
        # Set current selection
        date_index = self.date_combo.findText(self.filter_state["date_range"])
        if date_index >= 0:
            self.date_combo.setCurrentIndex(date_index)
        
        self.form_layout.addRow(date_label, self.date_combo)
        
        # Payment method filter
        payment_label = QtWidgets.QLabel("Payment Method:")
        self.payment_combo = QtWidgets.QComboBox()
        self.payment_combo.addItem("All Methods")
        
        # Get unique payment methods
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT payment_method 
                FROM transactions 
                WHERE payment_method IS NOT NULL AND payment_method != ''
            """)
            methods = cursor.fetchall()
            for method in methods:
                if method['payment_method']:
                    self.payment_combo.addItem(method['payment_method'])
            cursor.close()
        except mysql.connector.Error:
            # Add defaults if DB connection fails
            self.payment_combo.addItems(["Cash", "Credit Card", "GCash", "PayMaya"])
        
        # Set current selection
        payment_index = self.payment_combo.findText(self.filter_state["payment_method"])
        if payment_index >= 0:
            self.payment_combo.setCurrentIndex(payment_index)
        
        self.form_layout.addRow(payment_label, self.payment_combo)
        
        # Amount range filter
        amount_label = QtWidgets.QLabel("Amount Range:")
        self.amount_combo = QtWidgets.QComboBox()
        self.amount_combo.addItems([
            "All Amounts",
            "Under ₱500",
            "₱500 - ₱1,000",
            "₱1,000 - ₱2,500",
            "₱2,500 - ₱5,000",
            "Over ₱5,000"
        ])
        
        # Set current selection
        amount_index = self.amount_combo.findText(self.filter_state["amount_range"])
        if amount_index >= 0:
            self.amount_combo.setCurrentIndex(amount_index)
        
        self.form_layout.addRow(amount_label, self.amount_combo)
        
        # Service filter
        service_label = QtWidgets.QLabel("Service:")
        self.service_combo = QtWidgets.QComboBox()
        self.service_combo.addItem("All Services")
        
        # Get unique services
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT s.service_name 
                FROM services s
                INNER JOIN transactions t ON s.service_id = t.service_id
                WHERE s.service_name IS NOT NULL AND s.service_name != ''
            """)
            services = cursor.fetchall()
            for service in services:
                if service['service_name']:
                    self.service_combo.addItem(service['service_name'])
            cursor.close()
        except mysql.connector.Error:
            pass
        
        # Set current selection
        service_index = self.service_combo.findText(self.filter_state["service"])
        if service_index >= 0:
            self.service_combo.setCurrentIndex(service_index)
        
        self.form_layout.addRow(service_label, self.service_combo)
        
        # Helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Combine filters to analyze sales patterns and identify top-performing services by time period and payment method."
        )
        helper_text.setStyleSheet("color: #4FC3F7; font-style: italic; font-size: 12px;")
        helper_text.setWordWrap(True)
        self.form_layout.addRow(helper_text)
        
        # Update button text
        self.save_button.setText("Apply Filter")
        self.save_button.clicked.connect(self.apply_filters)
        
        # Add reset button
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.reset_button.clicked.connect(self.reset_filters)
        
        # Insert reset button into layout
        self.button_layout.insertWidget(self.button_layout.count() - 2, self.reset_button)
    
    def apply_filters(self):
        """Apply selected filters"""
        self.result_filter_state["date_range"] = self.date_combo.currentText()
        self.result_filter_state["payment_method"] = self.payment_combo.currentText()
        self.result_filter_state["amount_range"] = self.amount_combo.currentText()
        self.result_filter_state["service"] = self.service_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["date_range"] != "All Time" or
            self.result_filter_state["payment_method"] != "All Methods" or
            self.result_filter_state["amount_range"] != "All Amounts" or
            self.result_filter_state["service"] != "All Services"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "amount_range": "All Amounts",
            "service": "All Services"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state